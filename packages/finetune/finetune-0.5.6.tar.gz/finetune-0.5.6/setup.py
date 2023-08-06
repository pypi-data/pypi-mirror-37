"""
IndicoAPI setup
"""
import os
import atexit
import urllib
import urllib.request
from sys import version_info
from setuptools import setup, find_packages
from setuptools.command.install import install
from pathlib import Path


def download_data_if_required():
    """ Pulls the pre-trained model weights from Github if required. """
    github_base_url = "https://raw.githubusercontent.com/IndicoDataSolutions/finetune/master/finetune/model/"
    s3_base_url = "https://s3.amazonaws.com/bendropbox/"

    file_list = [
        (github_base_url, "encoder_bpe_40000.json"),
        (github_base_url, "vocab_40000.bpe"),
        (s3_base_url, "Base_model.jl"),
        (s3_base_url, "SmallBaseModel.jl")
    ]

    for root_url, filename in file_list:
        folder = os.path.abspath(os.path.join('finetune', 'model'))
        if not os.path.exists(folder):
            os.mkdir(folder)

        local_filepath = os.path.join(folder, filename)

        if not Path(local_filepath).exists():
            print("Downloading: {}".format(local_filepath))
            data = urllib.request.urlopen(root_url + filename).read()
            fd = open(local_filepath, 'wb')
            fd.write(data)
            fd.close()


def _post_install():
    """
    Run as last step of setup.py
    """
    download_data_if_required()


class SetupInstall(install):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        atexit.register(_post_install)


REQUIREMENTS = [
    "pandas>=0.23.1",
    "IndicoIo>=1.1.5",
    "tqdm>=4.0.0",
    "numpy>=1.13.0",
    "scipy>=1.1.0",
    "scikit-learn>=0.18.0",
    "ftfy>=4.4.0",
    "spacy>=2.0.0",
    "msgpack-numpy==0.4.1",
    "h5py>=2.8.0",
    "joblib>=0.12.0",
    "bs4>=0.0.1",
    "imblearn>=0.0"
]

setup(
    name="finetune",
    packages=find_packages(),
    version="0.5.6",
    install_requires=REQUIREMENTS,
    include_package_data=False,
    cmdclass={
        'install': SetupInstall,
        'develop': SetupInstall
    }
)
