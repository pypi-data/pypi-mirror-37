from unittest import TestCase

from pathlib import Path
from ..loaded_strpipe import LoadedStrpipe


class LoadedStrpipeTestCase(TestCase):

    def setUp(self):
        self.strpipe_json_path = str(
            Path(__file__).resolve().parent.joinpath('data/example.json'))
        self.maxlen = 7
        self.indexer = LoadedStrpipe(
            path=self.strpipe_json_path,
        )
        self.input_data = [
            '克安是牛肉大粉絲',
            '繼良喜歡喝星巴巴',
            '安靜的祥睿',
        ]

    def test_correctly_init(self):
        self.assertFalse(self.indexer.is_built)

    def test_build(self):
        self.indexer.build()
        self.assertTrue(self.indexer.is_built)

    def test_transform(self):
        self.indexer.build()
        tx_data, meta, _ = self.indexer.transform(self.input_data)
        self.assertEqual(
            [
                [4, 5, 3, 3, 3, 3, 3],
                [3, 3, 3, 3, 3, 6, 7],
                [5, 8, 3, 10, 3, 3, 3],
            ],
            tx_data,
        )

    def test_inverse_transform(self):
        self.indexer.build()
        tx_data, meta, _ = self.indexer.transform(self.input_data)
        output = self.indexer.inverse_transform(tx_data, meta)
        self.assertEqual(
            output,
            self.input_data,
        )
