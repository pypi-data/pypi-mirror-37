import gensim
import torch
from typing import Union, List

from gensim.models import KeyedVectors

from flair.data import TaggedCorpus, Sentence, Token
from flair.embeddings import TokenEmbeddings, StackedEmbeddings, CharLMEmbeddings
from flair.file_utils import cached_path


class DomainModeEmbeddings(TokenEmbeddings):

    def __init__(self, contextual_embeddings: CharLMEmbeddings, corpus: TaggedCorpus):
        super().__init__()

        self.embedding_length = contextual_embeddings.embedding_length
        self.name = contextual_embeddings.name + '-context'

        # first, make pass over corpus to produce embeddings
        word_embeddings = {}
        word_count = {}

        sentences = corpus.train + corpus.test + corpus.dev

        mini_batch_size: int = 100
        batches = [sentences[x:x + mini_batch_size] for x in range(0, len(sentences), mini_batch_size)]

        for batch in batches:

            contextual_embeddings.embed(batch)
            for sentence in batch:
                for token in sentence:
                    if token.text not in word_embeddings:
                        word_embeddings[token.text] = token.embedding.cpu()
                        word_count[token.text] = 1
                    else:
                        word_embeddings[token.text] = torch.add(word_embeddings[token.text], token.embedding)
                        word_count[token.text] += 1
                sentence.clear_embeddings()

        sorted_by_value = sorted(word_count.items(), key=lambda kv: kv[1], reverse=True)

        count = len(sorted_by_value)

        base_path = ''
        vector_file = base_path + contextual_embeddings.name + '-tmp.vec'
        with open(vector_file, 'w') as f:
            f.write('{} {}\n'.format(count, contextual_embeddings.embedding_length))
            for idx, word in enumerate(sorted_by_value):
                embedding = word_embeddings[word[0]] / word[1]
                vector = ' '.join(str(v) for v in embedding.tolist())
                f.write('{} {}\n'.format(word[0], vector))

        vectors = gensim.models.KeyedVectors.load_word2vec_format(vector_file, binary=False)
        base_embeddings_file = base_path + contextual_embeddings.name + '-multimod'
        vectors.save(base_embeddings_file, pickle_protocol=4)

        self.base_embeddings: KeyedVectors = gensim.models.KeyedVectors.load(base_embeddings_file)
        self.context_embeddings: CharLMEmbeddings = contextual_embeddings

    def embed(self, sentences: Union[Sentence, List[Sentence]]):

        self.context_embeddings.embed(sentences)

        for sentence in sentences:
            for token in sentence.tokens:
                base = self.base_embeddings.get_vector(token.text)

                # contextualized_embedding = token._embeddings[self.context_embeddings.name] * torch.FloatTensor(base)
                contextualized_embedding = (token._embeddings[self.context_embeddings.name] + torch.FloatTensor(base)) / 2

                del token._embeddings[self.context_embeddings.name]
                token.set_embedding(self.name, contextualized_embedding)

    def embedding_length(self) -> int:
        return self.embedding_length

class OnePassStoreEmbeddings(TokenEmbeddings):
    def __init__(self, embedding_stack: StackedEmbeddings, corpus: TaggedCorpus, detach: bool = True):
        super().__init__()

        self.embedding_stack = embedding_stack
        self.detach = detach
        self.name = 'Stack'
        self.static_embeddings = True

        self.embedding_length: int = embedding_stack.embedding_length
        print(self.embedding_length)

        sentences = corpus.get_all_sentences()
        mini_batch_size: int = 32
        sentence_no: int = 0
        written_embeddings: int = 0

        total_count = 0
        for sentence in sentences:
            for token in sentence.tokens:
                total_count += 1

        embeddings_vec = 'fragment_embeddings.vec'
        with open(embeddings_vec, 'w') as f:

            f.write('%d %d\n' % (total_count, self.embedding_stack.embedding_length))

            batches = [sentences[x:x + mini_batch_size] for x in
                       range(0, len(sentences), mini_batch_size)]

            for batch in batches:

                self.embedding_stack.embed(batch)

                for sentence in batch:
                    sentence: Sentence = sentence
                    sentence_no += 1

                    for token in sentence.tokens:
                        token: Token = token

                        signature = self.get_signature(token)
                        vector = token.get_embedding().data.numpy().tolist()
                        vector = ' '.join(map(str, vector))
                        vec = signature + ' ' + vector
                        written_embeddings += 1
                        token.clear_embeddings()

                        f.write('%s\n' % vec)

                print('%d\t(%d)' % (sentence_no, written_embeddings))

        vectors = gensim.models.KeyedVectors.load_word2vec_format(embeddings_vec, binary=False)
        vectors.save('stored_embeddings', pickle_protocol=4)
        # import os
        # os.remove('fragment_embeddings.vec')
        vectors = None

        self.embeddings = gensim.models.KeyedVectors.load('stored_embeddings')

    def get_signature(self, token: Token) -> str:
        context: str = ' '
        for i in range(token.idx - 4, token.idx + 5):
            if token.sentence.get_token(i) is not None:
                context += token.sentence.get_token(i).text + ' '
        signature = '{}··{}:··{}'.format(token.text, token.idx, context)
        return signature.strip().replace(' ', '·')

    def embed(self, sentences: Union[Sentence, List[Sentence]]):

        for sentence in sentences:
            for token in sentence.tokens:
                signature = self.get_signature(token)
                word_embedding = self.embeddings[signature]
                word_embedding = torch.autograd.Variable(torch.FloatTensor(word_embedding))
                token.set_embedding(self.name, word_embedding)

    def embedding_length(self) -> int:
        return self.embedding_length

    def _add_embeddings_internal(self, sentences: List[Sentence]):
        return sentences

    def __getstate__(self):
        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        del state['embeddings']
        return state


class WindowContextEmbeddings(TokenEmbeddings):
    """Contextual string embeddings of words, as proposed in Akbik et al., 2018."""

    def __init__(self, model, window_size: int = 5, detach: bool = True):
        """
            Contextual string embeddings of words, as proposed in Akbik et al., 2018.

            Parameters
            ----------
            arg1 : model
                model string, one of 'news-forward', 'news-backward', 'mix-forward', 'mix-backward', 'german-forward',
                'german-backward' depending on which character language model is desired
            arg2 : detach
                if set to false, the gradient will propagate into the language model. this dramatically slows down
                training and often leads to worse results, so not recommended.
        """
        super().__init__()

        # news-english-forward
        if model.lower() == 'news-forward':
            base_path = 'https://s3.eu-central-1.amazonaws.com/alan-nlp/resources/embeddings/lm-news-english-forward-v0.2rc.pt'
            model = cached_path(base_path, cache_dir='embeddings')

        # news-english-backward
        if model.lower() == 'news-backward':
            base_path = 'https://s3.eu-central-1.amazonaws.com/alan-nlp/resources/embeddings/lm-news-english-backward-v0.2rc.pt'
            model = cached_path(base_path, cache_dir='embeddings')

        # news-english-forward
        if model.lower() == 'news-forward-fast':
            base_path = 'https://s3.eu-central-1.amazonaws.com/alan-nlp/resources/embeddings/lm-news-english-forward-1024-v0.2rc.pt'
            model = cached_path(base_path, cache_dir='embeddings')

        # news-english-backward
        if model.lower() == 'news-backward-fast':
            base_path = 'https://s3.eu-central-1.amazonaws.com/alan-nlp/resources/embeddings/lm-news-english-backward-1024-v0.2rc.pt'
            model = cached_path(base_path, cache_dir='embeddings')

        # mix-english-forward
        if model.lower() == 'mix-forward':
            base_path = 'https://s3.eu-central-1.amazonaws.com/alan-nlp/resources/embeddings/lm-mix-english-forward-v0.2rc.pt'
            model = cached_path(base_path, cache_dir='embeddings')

        # mix-english-backward
        if model.lower() == 'mix-backward':
            base_path = 'https://s3.eu-central-1.amazonaws.com/alan-nlp/resources/embeddings/lm-mix-english-backward-v0.2rc.pt'
            model = cached_path(base_path, cache_dir='embeddings')

        # mix-german-forward
        if model.lower() == 'german-forward':
            base_path = 'https://s3.eu-central-1.amazonaws.com/alan-nlp/resources/embeddings/lm-mix-german-forward-v0.2rc.pt'
            model = cached_path(base_path, cache_dir='embeddings')

        # mix-german-backward
        if model.lower() == 'german-backward':
            base_path = 'https://s3.eu-central-1.amazonaws.com/alan-nlp/resources/embeddings/lm-mix-german-backward-v0.2rc.pt'
            model = cached_path(base_path, cache_dir='embeddings')

        self.name = model
        self.static_embeddings = detach

        from flair.models import LanguageModel
        self.lm = LanguageModel.load_language_model(model)
        self.detach = detach

        self.is_forward_lm: bool = self.lm.is_forward_lm

        dummy_sentence: Sentence = Sentence()
        dummy_sentence.add_token(Token('hello'))
        embedded_dummy = self.embed(dummy_sentence)
        self.__embedding_length: int = len(embedded_dummy[0].get_token(1).get_embedding())

    @property
    def embedding_length(self) -> int:
        return self.__embedding_length

    def _add_embeddings_internal(self, sentences: List[Sentence]) -> List[Sentence]:

        contexts: List[str] = []
        offsets: List[int] = []
        all_tokens: List[Token] = []
        for sentence in sentences:
            for token in sentence:

                all_tokens.append(token)

                context = ''
                window_size = 5
                for i in range(window_size + 1):
                    # print(token.idx - i)
                    context_token = sentence.get_token(token.idx - i) if self.is_forward_lm else sentence.get_token(
                        token.idx + i)
                    # print(context_token)
                    if context_token is not None:
                        text = context_token.text if self.is_forward_lm else context_token.text[::-1]
                        context = text + ' ' + context
                    else:
                        context = '\n' + context

                contexts.append(context)
                offsets.append(len(context) - 1)

        longest_character_sequence_in_batch: int = len(max(contexts, key=len))

        # pad strings with whitespaces to longest sentence
        contexts_padded: List[str] = []
        append_context = contexts_padded.append

        # print(contexts)

        end_marker = ''
        for context in contexts:
            pad_by = longest_character_sequence_in_batch - len(context)
            # if self.is_forward_lm:
            padded = '{}{}{}'.format(context, end_marker, pad_by * ' ')
            append_context(padded)
            # else:
            # padded = '{}{}{}'.format(context[::-1], end_marker, pad_by * ' ')
            # append_context(padded)

        # get hidden states from language model
        all_hidden_states_in_lm = self.lm.get_representation(contexts_padded, self.detach)

        # take first or last hidden states from language model as word representation
        i = 0
        for token, offset, context in zip(all_tokens, offsets, contexts_padded):
            token: Token = token

            # print('c: "{}"'.format(context))
            # print(token.text)
            # print(offset)
            # print()

            embedding = all_hidden_states_in_lm[offset, i, :]

            token.set_embedding(self.name, embedding)
            i += 1

        return sentences
