from typing import List, Tuple

from abc import abstractmethod, ABC


class BaseIndexer(ABC):

    def __init__(self):
        self.is_built = False

    @abstractmethod
    def build(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def transform(
            self,
            data: List[str],
        ) -> Tuple[List[List[int]], dict]:
        """Transform strings to indices"""
        raise NotImplementedError

    @abstractmethod
    def inverse_transform(
            self,
            data: List[List[int]],
        ) -> List[str]:
        """Restore indices to strings"""
        raise NotImplementedError
