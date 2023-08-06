import os

RESOURCES_PATH_NAME = 'RESOURCES_PATH'
RESOURCES_PATH = os.environ.get(RESOURCES_PATH_NAME)
if RESOURCES_PATH is None:
    raise ValueError(
        f'Environment variable {RESOURCES_PATH_NAME} must be set before importing text-indexer',
    )
