import os
import json
from os.path import splitext, basename, join
import tarfile
import requests
import yaml


class TokenAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = 'Token ' + self.token
        return r

def load_yaml(task_path):
    with open(task_path) as f:
        config = None
        filename, file_extension = splitext(basename(task_path))
        if file_extension == ".json":
            config = json.load(f)
        elif file_extension == ".yaml":
            config = yaml.load(f)
        else:
            raise ValueError("{} is not a valid config".format(str(f)))
    return config


def make_tarfile(output_filename, source_dir):
    if not source_dir.endswith(os.path.sep):
        source_dir = source_dir + os.path.sep
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def unzip_tarfile(source_tar, target_dir):
    tar = tarfile.open(source_tar, "r:gz")
    tar.extractall(path=target_dir)
    tar.close()
