from typing import Optional
from gpt_index import GPTSimpleVectorIndex, SimpleDirectoryReader

import os


class PlurigridReader:
    def load(self, data_dir: str, index_path: Optional[str]):
        self.INDEX_PATH = index_path
        self.DATA_DIR = data_dir
        if index_path != None and os.path.exists(index_path):
            print("loading index from disk...")
            self.index = GPTSimpleVectorIndex.load_from_disk(index_path)
        else:
            print("initializing index, this may take a moment...")
            documents = SimpleDirectoryReader(data_dir).load_data()
            index = GPTSimpleVectorIndex(documents)
            index.save_to_disk(index_path)

    def query(self, question):
        res = self.index.query(question)
        return res.response
