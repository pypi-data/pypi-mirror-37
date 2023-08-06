import argparse
import sys
from ddlcli.job import submit_job, download_model_output
from ddlcli.user import register_user


def main():
    master_endpoint = "http://dtf-masterserver-dev.us-west-1.elasticbeanstalk.com"
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--task_config',
        type=str,
        help='Path to the training task configuration')

    parser.add_argument(
        '--master_endpoint_override',
        type=str,
        help='override to master server for submitting job')

    FLAGS, _ = parser.parse_known_args()

    invalid_function_msg = "Please provide the name of function. Support functions are: \n" \
                           "\t submit: submit a training job"
    try:
        if len(sys.argv) < 2:
            assert (len(sys.argv) > 2), invalid_function_msg
        function_name = sys.argv[1]

        if FLAGS.master_endpoint_override is not None:
            master_endpoint = FLAGS.master_endpoint_override

        if function_name == "submit":
            assert (FLAGS.task_config is not None), "task_config is a required argument"
            submit_job(FLAGS.task_config, master_endpoint)
        elif function_name == "register":
            register_user(master_endpoint)
        elif function_name == "progress":
            pass
        elif function_name == "download":
            assert (FLAGS.task_config is not None), "task_config is a required argument"

            parser.add_argument(
                '--job_uuid',
                type=str,
                required=True,
                help='Your job uuid shown when you submit a training job')

            parser.add_argument(
                '--dest',
                type=str,
                required=True,
                help='Your job uuid shown when you submit a training job')

            FLAGS, _ = parser.parse_known_args()
            download_model_output(master_endpoint, FLAGS.job_uuid, FLAGS.dest, FLAGS.task_config)
        else:
            assert False, invalid_function_msg
    except Exception as e:
        print(str(e))
