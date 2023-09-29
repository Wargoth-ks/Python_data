
import argparse
import logging
import re

from pathlib import Path
from time import time
from transliterate import translit
from shutil import copyfile
from concurrent.futures import ThreadPoolExecutor

TYPES = {
    "documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"],
    "audio": [".mp3", ".ogg", ".wav", ".amr", ".flac"],
    "video": [".avi", ".mp4", ".mov", ".mkv"],
    "images": [".jpeg", ".png", ".jpg", ".svg"],
    "archives": [".zip", ".gz", ".tar", ".rar"],
}

parser = argparse.ArgumentParser(description="This is file sorter", add_help=True)
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-o", "--output", default="dist")

args = vars(parser.parse_args())

source = args.get("input")
dest = args.get("output")

folders = []


def normalize(name):
    trans_name = translit(name, 'ru', reversed=True)
    pattern = r"[^\w\.]"
    trans_name = re.sub(pattern, "_", trans_name.lower().capitalize())
    return trans_name

def process_folder(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            process_folder(el)


def copy_files(path: Path):
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix.lower()
            
            copied = False
            for key, val in TYPES.items():
                if ext in val:
                    new_path = output_folder / key
                    try:
                        new_path.mkdir(exist_ok=True, parents=True)
                        copyfile(el, new_path / normalize(el.name))
                        print(f"<<{normalize(el.name)}>> скопійовано у <<{new_path}>>\n")
                        copied = True
                    except OSError as err:
                        logging.error(err)

            if not copied:
                unknown = Path().joinpath("unknown")
                other_path = output_folder / unknown
                try:
                    other_path.mkdir(exist_ok=True, parents=True)
                    copyfile(el, other_path / normalize(el.name))
                    print(f"<<{normalize(el.name)}>> скопійовано у <<{other_path}>>\n")
                except OSError as err:
                    logging.error(err)


if __name__ == "__main__":
    start_time = time()

    logging.basicConfig(level=logging.ERROR, format="%(threadName)s %(message)s")
    base_folder = Path(source)
    output_folder = Path(dest)
    folders.append(base_folder)
    process_folder(base_folder)

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(copy_files, folders)

    end_time = time()  # Засекаем время окончания выполнения программы
    total_time = end_time - start_time  # Вычисляем общее время выполнения
    print(f"Загальний час виконання: {total_time} секунд")
