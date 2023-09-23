
# This program sorted files

from move_files.move_files import move_files
from normalize.normalize import normalize
from pathlib import Path
import sys

folder_path = Path(sys.argv[1])

print("\nStarting sort Thrash folder...\n")

# This function search all folders and files and use normalize function


def process_folder(folder_path: Path):

    for dirs in folder_path.iterdir():
        if dirs.is_dir():
            new_name = normalize(dirs.name)
            new_path = dirs.with_name(new_name)
            dirs.rename(new_path)
            process_folder(new_path)
        else:
            new_name = normalize(dirs.name)
            new_path = dirs.with_name(new_name)
            if new_path != dirs:
                dirs.rename(new_path)
            move_files(new_path)


# process_folder(Path(sys.argv[1]))
