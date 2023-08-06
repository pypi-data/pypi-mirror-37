from unittest import TestCase

from pathlib import Path
from ..char_with_word2vec import CharwtWord2Vec


class CharwtWord2VecTestCase(TestCase):

    def setUp(self):
        self.maxlen = 7
        self.indexer = CharwtWord2Vec(
            word2vec_path=str(
                Path(__file__).resolve().parent.joinpath('data/example.msg')),
            maxlen=self.maxlen,
        )
        self.input_data = [
            '克安是牛肉大粉絲',  # longer than 7 after adding sos eos
            '繼良喜歡喝星巴巴',  # longer than 7 after adding sos eos
            '安靜的祥睿',  # equal to 7 after adding sos eos
            '喔',  # shorter than 7 after adding sos eos
        ]

    def test_correctly_init(self):
        self.assertFalse(self.indexer.is_built)

    def test_build(self):
        self.indexer.build()
        self.assertTrue(self.indexer.is_built)
        self.assertEqual(
            set(['token2index', 'vector']),
            set(self.indexer.word2vec.keys()),
        )

    def test_transform(self):
        self.indexer.build()
        tx_data, meta = self.indexer.transform(self.input_data)
        self.assertEqual(
            [
                [0, 4, 5, 3, 3, 3, 3],
                [0, 3, 3, 3, 3, 3, 6],
                [0, 5, 8, 3, 10, 3, 1],
                [0, 3, 1, 3, 3, 3, 3],
            ],
            tx_data,
        )

        self.assertEqual(
            [7, 7, 7, 3],
            meta['seqlen'],
        )

    def test_inverse_transform(self):
        self.indexer.build()
        tx_data, meta = self.indexer.transform(self.input_data)
        output = self.indexer.inverse_transform(tx_data, meta['inv_info'])
        self.assertEqual(
            output,
            self.input_data,
        )

    def test_get_embedding(self):
        self.indexer.build()
        output = self.indexer.get_embedding()
        self.assertEqual(
            len(self.indexer.word2vec['token2index']),
            len(output),
        )
