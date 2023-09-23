from pathlib import Path
from shutil import move, unpack_archive
import sys

MUZ = []
VIDS = []
IMGS = []
DOCS = []
ARCHS = []
UNKNS = []


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
    for empty in Path(sys.argv[1]).rglob('*'):
        if empty.is_dir() and not any(empty.iterdir()):
            empty.rmdir()
            print(f"\nDelete empty << {empty.name} >> folder from Thrash\n")
