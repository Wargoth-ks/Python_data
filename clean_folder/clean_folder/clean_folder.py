
# This program sorted files

from pathlib import Path
from shutil import move, unpack_archive
import sys
import re

print("\nStarting sort Thrash folder...\n")


MUZ = []
VIDS = []
IMGS = []
DOCS = []
ARCHS = []
UNKNS = []


folder_path = Path(sys.argv[1])

# Transliterate function


def normalize(name):
    trans_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g',
        'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
        'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
        'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c',
        'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '',
        'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu',
        'я': 'ya', 'А': 'A', 'Б': 'B', 'В': 'V',
        'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo',
        'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'J',
        'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
        'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S',
        'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H',
        'Ц': 'C', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch',
        'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E',
        'Ю': 'Yu', 'Я': 'Ya'
    }

    trans_name = ""

    pattern = r"[^\w\.]"
    re_name = re.sub(pattern, "_", name.lower().capitalize())

    for symb in re_name:
        if symb in trans_dict:
            trans_name += trans_dict[symb]
        else:
            trans_name += symb

    return trans_name

# This function doing some operations with files and folders


def move_files(new_path: Path):

    target_folder = Path("Sorted")

    # Transform suffix to lower symbols
    sufx = new_path.suffix.lower()

    # Find suffix and add folder
    if sufx in [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"]:
        ext_files = 'documents'
        DOCS.append(new_path.suffix)
    elif sufx in [".jpeg", ".png", ".jpg", ".svg"]:
        ext_files = 'images'
        IMGS.append(new_path.suffix)
    elif sufx in [".mp3", ".ogg", ".wav", ".amr"]:
        ext_files = 'music'
        MUZ.append(new_path.suffix)
    elif sufx in [".avi", ".mp4", ".mov", ".mkv"]:
        ext_files = 'video'
        VIDS.append(new_path.suffix)
    elif sufx in [".zip", ".gz", ".tar"]:
        ext_files = 'archives'
        ARCHS.append(new_path.suffix)
    else:
        ext_files = 'unknown'
        UNKNS.append(new_path.suffix)

    # Create folder in path to Sort/...
    sort_path = target_folder / ext_files  # Sorted / {documents, ...}
    sort_path.mkdir(exist_ok=True, parents=True)  # Make dirs
    dest_path = sort_path / f'{new_path.name}'

    # Move files to the folder of destination
    move(new_path, dest_path)
    print(f'-- File -- {new_path.name} was moved to {sort_path.name}')

    # Unpack archives
    if new_path.suffix in [".zip", ".gz", ".tar"]:
        arch_path = f'{sort_path}/{new_path.stem}'
        unpack_archive(f'{dest_path}', arch_path)
        print(f'\n\"\" {new_path.name} \"\" unpacked successfully !!!\n')

    # If folders are empty - delete its
    for empty in folder_path.rglob('*'):
        if empty.is_dir() and not any(empty.iterdir()):
            empty.rmdir()
            print(f"\nDelete empty << {empty.name} >> folder from Thrash\n")

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


def main():
    # Check command arguments
    try:
        if len(sys.argv) != 2:
            print("Usage: clean-folder /path/to/folder")
            sys.exit(1)
        else:
            process_folder(folder_path)

            print(f"\nMusic: {MUZ}")
            print(f"Video: {VIDS}")
            print(f"Images: {IMGS}")
            print(f"Documents: {DOCS}")
            print(f"Archives: {ARCHS}")
            print(f"Unknowns: {UNKNS}")
            print(
                "\nThis program has completed all necessary operations and terminated successfully.\n")

    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
