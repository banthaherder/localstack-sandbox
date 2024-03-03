import os
from operator import itemgetter
import boto3


def get_deploy_creation_times(bucket_name, s3_resource):
    bucket = s3_resource.Bucket(bucket_name)
    objects = bucket.objects.all()

    dir_creation_times = {}
    print(objects)

    # by default this will process objects in batches of 1000
    for obj in objects:
        top_level_dir = obj.key.split("/")[0]

        # use the object's last_modified attribute as the creation time
        creation_time = obj.last_modified

        # create a list of directories and note thier creation time
        if (
            top_level_dir not in dir_creation_times
            or creation_time < dir_creation_times[top_level_dir]
        ):
            dir_creation_times[top_level_dir] = creation_time

    for dir_name, creation_time in dir_creation_times.items():
        print(f"Directory: {dir_name}, Creation Time: {creation_time}")

    return dir_creation_times


def delete_deploy_dirs(
    bucket_name, dir_creation_times, keep_n_deploys, s3_resource_client
):
    bucket = s3_resource_client.Bucket(bucket_name)

    # sort directories by their creation times in descending order (latest first)
    sorted_dirs = sorted(dir_creation_times.items(), key=itemgetter(1), reverse=True)

    # identify directories to delete (all but the latest n)
    dirs_to_delete = [dir_name for dir_name, _ in sorted_dirs[keep_n_deploys:]]

    for dir_name in dirs_to_delete:
        print(f"[INFO] - deleting directory: {dir_name}")
        for obj in bucket.objects.filter(Prefix=f"{dir_name}/"):
            obj.delete()

    print(f"[INFO] - deleted {len(dirs_to_delete)} directories")


def lambda_handler(event, context):
    region = os.environ.get("AWS_REGION", "us-east-1")
    endpoint_url = os.environ.get("ENDPOINT_URL", "http://localhost:4566")

    bucket_name = event["bucket_name"]
    keep_n_deploys = event["keep_n_deploys"]

    s3_client = boto3.client("s3", endpoint_url=endpoint_url, region_name=region)
    s3_resource_client = boto3.resource(
        "s3", endpoint_url=endpoint_url, region_name=region
    )

    deploy_creation_times = get_deploy_creation_times(bucket_name, s3_resource_client)

    delete_deploy_dirs(
        bucket_name, deploy_creation_times, keep_n_deploys, s3_resource_client
    )


# local testing
if __name__ == "__main__":
    bucket_name = "sure-thing"
    keep_n_deploys = 5

    lambda_handler({"bucket_name": bucket_name, "keep_n_deploys": keep_n_deploys}, None)
