from setuptools import setup, find_packages

setup(
    name="clean_folder",
    version="0.1.0",
    packages=find_packages(),
    description='This program sorting thrash folder',
    url='https://github.com/Wargoth-ks/Python_data/tree/main/clean_folder',
    author='Wargoth_ks',
    author_email='warheart1986@gmail.com',
    license='MIT',
    entry_points={
        "console_scripts": [
            "clean-folder = clean_folder.clean_folder:main"
        ],
    },
)
