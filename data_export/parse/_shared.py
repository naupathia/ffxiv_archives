import pathlib
import csv 
import uuid
from data_export.settings import DATA_PATH

def iter_dir_files(dir_path):
    
    dir = pathlib.Path(dir_path)

    for f in dir.iterdir():
        if f.is_dir():
            for file_path in f.iterdir():
                yield file_path


def open_csv_for_iteration(filepath):
    fh = open(filepath, 'rt', encoding="UTF-8")
    fh.readline()

    return fh

def get_id():
    return str(uuid.uuid4())

def iter_csv_rows(file_path, skip_row_count=3):
    
    with open(file_path, 'rt', encoding="UTF-8") as fh:

        reader = csv.reader(fh)
        for line in reader:
            if skip_row_count > 0:
                skip_row_count -= 1
                continue

            yield line

class GameTypeRowAdapter:

    @classmethod
    def read_record(cls, row: dict):
        pass

class FileIterator:
    ADAPTER: GameTypeRowAdapter = None
    GAME_FILE: str = None 

    def __init__(self) -> None:
        self._iterator = None 
        self._fh = self._open_file()
        
        self.current = None
        self._iterator = csv.DictReader(self._fh)

        # skip the next record since it's data types for the columns
        next(self._iterator)

    def __iter__(self):
        return self 
    
    def __next__(self):
        
        try:
            self.current = None 

            while self.current is None:
                row = next(self._iterator)
                self.current = self._process_row(row)

            return self.current
        
        except StopIteration:
            self._fh.close()
            raise

    def _process_row(self, row: dict):
        result = self.ADAPTER.read_record(row)

        try:
            if result and "name" in result:
                if result["name"] in (None, '', '0'):
                    return None 
        except TypeError:
            print (result)
            raise 

        return result
    
    @classmethod
    def _open_file(cls):
        return open_csv_for_iteration(f"{DATA_PATH}\\{cls.GAME_FILE}")


class DirIterator:

    def __init__(self, dirname: str) -> None:
        
        self._iterator = (
            (filename, innerdirname.name)
            for innerdirname in pathlib.Path(f"{DATA_PATH}\\{dirname}").iterdir()
            for filename in pathlib.Path(innerdirname).iterdir()
        )
        
        self.current = None

    def __iter__(self):
        return self 
    
    def __next__(self):
        
        self.current = None 

        while self.current is None:
            filepath, dirname = next(self._iterator)
            self.current = self._process_file(filepath, dirname)

        return self.current
        

    def _process_file(self, filepath, dirname):
        pass