import json
import uuid
from os.path import isfile, isdir, exists, join, basename
import os
from time import sleep

import requests

from ddlcli.constants import CODE_DIR_NAME
from ddlcli.s3_util import create_s3_client, upload_dir_to_s3, upload_file_to_s3, download_files_from_s3
from ddlcli.user import login_user
from ddlcli.utils import load_yaml

from ddlcli.constants import DATASET_TAR_GZ
from ddlcli.utils import make_tarfile


def submit_job(task_path, master_endpoint):
    config = load_yaml(task_path)
    data = {
        'email': config["email"],
        'password': config["password"]
    }

    print("===========================================")
    print("Step 1: User login")
    print("===========================================")
    auth, s3_temp_token = login_user(data, master_endpoint)

    print("===========================================")
    print("Step 2: Submit task")
    print("===========================================")

    job_data = config["job_data"]

    submit_task(job_data, s3_temp_token, auth, master_endpoint)


def submit_task(job_data, s3_temp_token, auth, master_endpoint):
    validate_tf_param(job_data)

    # compress dataset
    dataset_tar_location = join(job_data["dataset"]["dataset_location"], DATASET_TAR_GZ)
    make_tarfile(dataset_tar_location, job_data["dataset"]["dataset_location"])

    code_location_s3, dataset_location_s3, requirement_location_s3 = upload_to_s3(
        job_data["model_location"],
        dataset_tar_location,
        job_data["requirement_location"],
        s3_temp_token['job_id'],
        s3_temp_token)

    print("job uuid on s3 is: {}".format(s3_temp_token['job_id']))

    if exists(dataset_tar_location):
        os.remove(dataset_tar_location)
    else:
        print("cannot find compressed dataset.tar.gz")

    job_data["model_location"] = code_location_s3
    job_data["dataset"]["dataset_location"] = dataset_location_s3
    job_data["requirement_location"] = requirement_location_s3

    print("model_location: {0}, dataset_location: {1}".format(job_data["model_location"],
                                                              job_data["dataset"]["dataset_location"]))

    request_body = {
        'parameters': json.dumps(job_data),
        'job_id': s3_temp_token['job_id']
    }

    create_task_request = requests.post("{}/api/v1/user/tf/job/".format(master_endpoint), data=request_body, auth=auth)
    create_task_resp = json.loads(create_task_request.text)
    print("Status: {}".format(create_task_request.status_code))
    if not create_task_request.ok:
        print("Error: {}".format(create_task_resp.get("error")))
        print("Message: {}".format(create_task_resp.get("message")))
        exit(-1)

    print("job_uuid: {}".format(create_task_resp.get("job_uuid")))
    print("job_type: {}".format(create_task_resp.get("job_type")))


def validate_tf_param(tf_param):
    model_location = tf_param["model_location"]
    if not isdir(model_location) and not isfile(model_location):
        raise ValueError("cannot find model path {}".format(model_location))

    dataset_location = tf_param["dataset"]["dataset_location"]
    if not isdir(dataset_location) and not isfile(dataset_location):
        raise ValueError("cannot find dataset path {}".format(dataset_location))

    if tf_param["worker_required"] <= 0:
        raise ValueError("number of workers cannot be less than or equal to 0")


def upload_to_s3(code_location, dataset_location, requirement_location, uuid, s3_temp_token):
    retry = 3
    latest_exception = None
    while retry > 0:
        try:
            client = create_s3_client(s3_temp_token)
            s3_bucket_name = s3_temp_token['s3_bucket_name']
            code_location_s3 = upload_dir_to_s3(code_location, s3_bucket_name, CODE_DIR_NAME, uuid, client)
            if isfile(dataset_location):
                folder_name = "{0}/{1}".format(uuid, "dataset")
                dataset_location_s3 = upload_file_to_s3(dataset_location, s3_bucket_name, folder_name, client)
            else:
                dataset_location_s3 = upload_dir_to_s3(dataset_location, s3_bucket_name, "dataset", uuid, client)

            requirement_location_s3 = upload_file_to_s3(requirement_location, s3_bucket_name, uuid, client)
            return code_location_s3, dataset_location_s3, requirement_location_s3

        except Exception as ex:
            latest_exception = str(ex)
            sleep(2)
            retry -= 1

    raise RuntimeError("failed to upload to s3 with exception: {}".format(latest_exception))


def download_model_output(master_endpoint, job_uuid, dest, task_path):
    config = load_yaml(task_path)
    data = {
        'email': config["email"],
        'password': config["password"],
        'job_id': job_uuid
    }

    print("===========================================")
    print("Step 1: User login")
    print("===========================================")
    _, s3_temp_token = login_user(data, master_endpoint)

    client = create_s3_client(s3_temp_token)
    if not exists(dest):
        os.makedirs(dest)
    elif not isdir(dest):
        raise Exception("{} is a file but not a directory".format(dest))

    s3_bucket_name = s3_temp_token['s3_bucket_name']
    download_files_from_s3(s3_bucket_name, job_uuid + "/out", dest, client)
    print("Finished download for job: {}".format(job_uuid))
