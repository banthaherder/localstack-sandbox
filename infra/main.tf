resource "aws_lambda_function" "deployment_janitor" {
  function_name = "deployment_janitor"
  handler       = "main.lambda_handler"
  runtime       = "python3.11"
  role          = aws_iam_role.deployment_janitor.arn

  filename = "../src/lambda_function.zip"

  environment {
    variables = {
        # override the endpoint url used for local testing
        ENDPOINT_URL = "s3.dualstack.us-east-1.amazonaws.com"
    }
  }
}

resource "aws_iam_role" "deployment_janitor" {
  name = "DeployJanitor"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Effect = "Allow"
        Sid    = ""
      },
    ]
  })
}

resource "aws_cloudwatch_event_rule" "daily_cleanup" {
  name                = "daily-deploy-janitor-trigger"
  description         = "Triggers Lambda at 7/8 AM PST/PDT daily"
  schedule_expression = "cron(0 15 * * ? *)" # 7/8 AM PST/PDT is 15:00 UTC
}

resource "aws_cloudwatch_event_target" "invoke_lambda" {
  rule      = aws_cloudwatch_event_rule.daily_cleanup.name
  target_id = "TriggerLambdaFunction"
  arn       = aws_lambda_function.deployment_janitor.arn

  input = jsonencode({
    bucket_name    = var.bucket_name
    keep_n_deploys = var.keep_n_deploys
  })
}

resource "aws_lambda_permission" "allow_event_bridge" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.deployment_janitor.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily_cleanup.arn
}
