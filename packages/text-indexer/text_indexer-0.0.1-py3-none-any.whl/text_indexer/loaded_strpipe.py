from typing import List, Tuple

import strpipe as sp

from .base import BaseIndexer


class LoadedStrpipe(BaseIndexer):

    def __init__(self, path: str):
        self._path = path
        super().__init__()

    def build(self):
        if not self.is_built:
            # restore strpipe
            self.pipe = sp.Pipe.restore_from_json(self._path)
            self.is_built = True

    def transform(
            self,
            utterances: List[str],
        ) -> Tuple[List[List[int]], List[dict]]:
        return self.pipe.transform(utterances)

    def inverse_transform(
            self,
            indices: List[List[int]],
            tx_info: List[dict],
        ) -> List[str]:
        return self.pipe.inverse_transform(indices, tx_info)
