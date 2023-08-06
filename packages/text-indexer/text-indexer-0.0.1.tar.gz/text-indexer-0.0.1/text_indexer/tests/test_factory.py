from unittest import TestCase

from pathlib import Path
from ..char_with_word2vec import CharwtWord2Vec
from ..factory import IndexerFactory


class IndexerFactoryTestCase(TestCase):

    def setUp(self):
        self.maxlen = 7

    def test_register_exists(self):
        factory = IndexerFactory()
        indexer = CharwtWord2Vec(
            word2vec_path=str(
                Path(__file__).resolve().parent.joinpath('data/example.msg')),
            maxlen=self.maxlen,
        )
        factory.register('test indexer', indexer)
        self.assertEqual(
            indexer,
            factory.indexers['test indexer'],
        )

    def test_regitster_already_exists(self):
        factory = IndexerFactory()
        indexer = CharwtWord2Vec(
            word2vec_path=str(
                Path(__file__).resolve().parent.joinpath('data/example.msg')),
            maxlen=self.maxlen,
        )
        factory.register('test indexer', indexer)
        with self.assertRaises(KeyError):
            factory.register('test indexer', indexer)

    def test_get_indexer_not_exists(self):
        factory = IndexerFactory()
        with self.assertRaises(KeyError):
            factory.get_indexer('some random key')

    def test_get_indexer_exists_correctly_also_build_indexer(self):
        factory = IndexerFactory()
        indexer = CharwtWord2Vec(
            word2vec_path=str(
                Path(__file__).resolve().parent.joinpath('data/example.msg')),
            maxlen=self.maxlen,
        )
        factory.register('test indexer', indexer)
        self.assertFalse(
            factory.indexers[factory.list_all()[0]].is_built,
        )
        self.assertEqual(
            indexer,
            factory.get_indexer('test indexer'),
        )
        self.assertTrue(indexer.is_built)

    def test__getitem__and__setitem(self):
        factory = IndexerFactory()
        indexer = CharwtWord2Vec(
            word2vec_path=str(
                Path(__file__).resolve().parent.joinpath('data/example.msg')),
            maxlen=self.maxlen,
        )
        factory['test indexer'] = indexer
        self.assertEqual(
            indexer,
            factory['test indexer'],
        )
