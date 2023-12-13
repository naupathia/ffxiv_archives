import pathlib
import csv 

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

    def __init__(self, fh) -> None:
        self._iterator = None 
        self._fh = fh
        
        self.current = None
        self._iterator = csv.DictReader(self._fh)

        # skip the next record since it's data types for the columns
        next(self._iterator)

    def __iter__(self):
        return self 
    
    def __next__(self):

        if not self._iterator:
            raise "Must use 'with' statement to initialize iterator"
        
        self.current = None 

        while self.current is None:
            row = next(self._iterator)
            self.current = self._process_row(row)

        return self.current

    def _process_row(self, row: dict):
        return self.ADAPTER.read_record(row)


class DirIterator:

    def __init__(self, dirname: str) -> None:
        self._iterator = None 
        self._dirname = dirname
        self._fh = None
        
        self.current = None

    def __iter__(self):
        return self 
    
    def __next__(self):

        if not self._iterator:
            raise "Must use 'with' statement to initialize iterator"
        
        self.current = None 

        while self.current is None:
            filepath = next(self._iterator)
            self.current = self._process_file(filepath)

        return self.current
        

    def _process_file(self, filepath):
        pass