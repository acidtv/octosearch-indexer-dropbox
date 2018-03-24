from setuptools import setup

setup(
        name='octosearch-indexer-dropbox',
        # packages=find_packages(),
        entry_points={
            'octosearch.indexer': [
                'dropbox = indexer:Indexer',
                ],
            },
        install_requires=[
            'octosearch',
            'dropbox',
            ]
        )
