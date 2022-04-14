import argparse
import json
import shutil
from collections import Counter, defaultdict
from ctypes import Union
from pathlib import Path
from typing import Union

from loguru import logger

from src.data import DATA_DIR
from src.utils.io import read_json


class organizer:
    """This class is used to organize files in a directory based on their extensions
    """

    def __init__(self):
        self.dir_ext_map = read_json(DATA_DIR/'extensions.json')

    def __call__(self, dir_path: Union[Path, str]):

        path = Path(dir_path)
        for entry in list(path.rglob('*.*')):
            extension = entry.suffix.replace('.', '')
            for dir_, ext_ in self.dir_ext_map.items():
                if extension in ext_:
                    dest = path/dir_
                    break
            else:
                dest = path/'others'

            dest.mkdir(parents=True, exist_ok=True)
            if not Path(dest/entry.name).exists():
                logger.info(f"moving {str(entry)} to {str(dest)}")
                shutil.move(str(entry), str(dest))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="A tool to extract Email addresses from a website")

    parser.add_argument("-d", "--dirpath", type=str,
                        required=True, metavar="", help="directory path to be organized")

    args = parser.parse_args()

    if Path(args.dirpath).exists():
        dir_organizer = organizer()
        dir_organizer(args.dirpath)
    else:
        raise FileNotFoundError("There is no such a directory")
