from os.path import join

from .factory import IndexerFactory
from .char_with_word2vec import CharwtWord2Vec

from .global_vars import RESOURCES_PATH


factory = IndexerFactory()
factory.register(
    name='SimpleCharToIndex',
    indexer=CharwtWord2Vec(
        word2vec_path=join(
            RESOURCES_PATH,
            'zh_char_fasttext_word2vec.msg',
        ),
    ),
)
