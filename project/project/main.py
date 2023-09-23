# This main function for run program

from clean_folder.clean_folder import process_folder, folder_path
from move_files.move_files import DOCS, IMGS, MUZ, VIDS, ARCHS, UNKNS

import sys


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
        print(f"This program was stopping with {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
