1. Where should we run this script?

For a recurring utility script like this I would recommend deploying a simple lambda wired up to EventBridge Scheduler. This gives us a light-weight, low maintenance service that is managed via AWS.

2. How should we test the script before running it production?

I hadn't used it before, but I found LocalStack to be remarkably useful for testing my solution. Once local development is completed and code has passed reviews we would look to test this against dev, stage, and any other existing testing environment before rolling it out to production. Additionally, [tflocal](https://github.com/localstack/terraform-local) can be used to test the infrastructure components.


3. If we want to add an additional requirement of deleting deploys older than X days but we must maintain at least Y number of deploys. What additional changes would you need to make in the script?

To support the additional requirement of preserving the last Y number of deploys we would look to add functionality that takes advantage of our sorted list of current deploys and their creation date to make a list of the Y number of deploys we should absolutely keep -- we'll call this list `deploys_to_preserve`. Then using the specified "delete deploys older than X days" create a list of deploys that would be deleted due to their age -- we'll call this list `old_deploys`. Now if the number of deploys in `len(old_deploys)` is more than `len(total_number_of_deploys) - len(deploys_to_preserve)` that means there is overlap and we must first compare and filter `old_deploys` against `deploys_to_preserve` before proceeding. If it's less than or equal, we are safe to proceed with deletion of the old deploys.

## How to Setup
1. run `docker compose up -d` (or `nerdctl compose up -d`) to bring localstack online
2. run `make bucket-up` to create a test bucket in localstack called "sure-thing". This will also seed the bucket with some dummy deploys and artifacts.
3. run `make run-janitor` to run a script that preserves the last 5 deploys in the default "sure-thing" bucket. These default settings can be modified by editing the main() in src/main.py.
4. run `make bucket-down` to delete the remaining bucket objects and deprovision the bucket.

## Deployment
1. zip src/main.py into src/lambda_function.py
2. run terraform init & terraform apply (**use tflocal to test against localstack)

## Improvements
Where do I even begin...
1. implement better logging using `logging` module
2. 