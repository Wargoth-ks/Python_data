from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='3.0.0',
    description='This program sorting thrash folder',
    url='http://github.com/dummy_user/clean_folder',
    author='Wargoth_ks',
    author_email='wargoth_ks@mail.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean-folder = project.main:main']} # running command = name_dir.name_main.py: name_main_func
)
