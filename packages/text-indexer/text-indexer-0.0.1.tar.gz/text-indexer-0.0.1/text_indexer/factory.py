from .base import BaseIndexer


class IndexerFactory:

    def __init__(self):
        self.indexers = {}

    def list_all(self):
        return list(self.indexers.keys())

    def register(self, name: str, indexer: BaseIndexer):
        if name in self.indexers:
            raise KeyError(
                f'Indexer [{name}] has existed. Please use another name',
            )
        self.indexers[name] = indexer

    def get_indexer(self, name):
        if name not in self.indexers:
            raise KeyError(
                f'Indexer [{name}] has not found.',
            )
        self.indexers[name].build()
        return self.indexers[name]

    def __getitem__(self, name):
        return self.get_indexer(name)

    def __setitem__(self, name, indexer):
        return self.register(name, indexer)
