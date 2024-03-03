import argparse
import boto3
import sys
import random
import time


# Function to create an S3 bucket
def create_bucket(bucket_name, s3):
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"[INFO] - bucket '{bucket_name}' created successfully")
        deploy_number = random.randint(1000, 9999)

        # TODO: parameterize the number of deploys to create
        for i in range(20):
            # create a deploy directory and add dummy deploy artifacts
            top_level_dir = f"deploy-{deploy_number + i}/"

            dummy_files = [
                "index.html",
                "bundle.js",
                "css/main.css",
                "fonts/fancy.ttf",
                "asssets/logo.png",
            ]

            for file_name in dummy_files:
                full_path = top_level_dir + file_name
                s3.put_object(Bucket=bucket_name, Key=full_path, Body=b"")

            print(f"[INFO] - dummy deploy '{top_level_dir}' created in bucket")
            # sleep to vary file creation time
            time.sleep(random.uniform(0.25, 2))

    except Exception as e:
        print(f"[ERROR] - failed to create bucket or add dummy files: {e}")
        sys.exit(1)


# Function to delete an S3 bucket
def delete_bucket(bucket_name, s3):
    try:
        bucket = s3.Bucket(bucket_name)
        bucket.objects.delete()
        bucket.delete()
        print(
            f"[INFO] - bucket '{bucket_name}' and all its contents deleted successfully"
        )
    except Exception as e:
        print(f"[ERROR] - failed to delete bucket: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="S3 Bucket Manager CLI")
    parser.add_argument(
        "--endpoint-url",
        default="http://localhost:4566",
        help="The endpoint URL for the S3 service (defaults to LocalStack)",
    )
    parser.add_argument("--create", metavar="BUCKET_NAME", help="Create an S3 bucket")
    parser.add_argument("--delete", metavar="BUCKET_NAME", help="Delete an S3 bucket")

    args = parser.parse_args()

    if args.create:
        s3_client = boto3.client(
            "s3", endpoint_url=args.endpoint_url, region_name="us-east-1"
        )
        create_bucket(args.create, s3_client)
    elif args.delete:
        s3_resource_client = boto3.resource(
            "s3", endpoint_url=args.endpoint_url, region_name="us-east-1"
        )
        delete_bucket(args.delete, s3_resource_client)
    else:
        print("[ERROR] - no valid action specified. Use --create or --delete")
        sys.exit(1)


if __name__ == "__main__":
    main()
