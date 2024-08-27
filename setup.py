from setuptools import setup, find_packages
import os
import pathlib

CURRENT_DIR = pathlib.Path(__file__).parent
README = (CURRENT_DIR / "README.md").read_text()

env = os.environ.get('source')


def get_dependencies():
    dependency = [
        'Flask-SQLAlchemy==3.1.1'
    ]

    if env and env == "code":
        return dependency

    return dependency + ["ppy-common"]


setup(
    name='pweb-orm',
    version='0.0.8',
    url='https://github.com/banglafighter/pweb-orm',
    license='Apache 2.0',
    author='Bangla Fighter',
    author_email='banglafighter.com@gmail.com',
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
