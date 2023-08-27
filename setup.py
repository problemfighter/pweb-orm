from setuptools import setup, find_packages
import os
import pathlib

CURRENT_DIR = pathlib.Path(__file__).parent
README = (CURRENT_DIR / "README.md").read_text()

env = os.environ.get('source')


def get_dependencies():
    dependency = [
        'Flask-SQLAlchemy', "ppy-common"
    ]

    if env and env == "dev":
        return dependency

    return dependency + []


setup(
    name='pweb-orm',
    version='1.0.0',
    url='https://github.com/problemfighter/pweb-orm',
    license='Apache 2.0',
    author='Problem Fighter',
    author_email='problemfighter.com@gmail.com',
    description='PWeb Object Relational Mapping Library, based on SQLAlchemy is an open-source SQL toolkit and object-relational mapper. It also used the Flask-SQLAlchemy extension.',
    long_description=README,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=get_dependencies(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ]
)
