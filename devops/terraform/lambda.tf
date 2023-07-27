data "aws_iam_policy_document" "lambda_trust_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_role" {
  name               = "example_lambda_role"
  assume_role_policy = data.aws_iam_policy_document.lambda_trust_policy.json
}

resource "aws_lambda_function" "autocompletion_comics_lambda" {
  function_name    = "autocompletion_comics_lambda"
  s3_bucket        = "autocompletion-comics-buckets"
  s3_key           = "lambda/lambda_function_payload.zip"
  role             = aws_iam_role.lambda_role.arn
  handler          = "app.lambda_handler" # The entry point to your Flask app
  runtime          = "python3.8"
  source_code_hash = filebase64sha256("lambda_function_payload.zip")

  environment {
    variables = {
    }
  }
}

resource "aws_api_gateway_rest_api" "comicsAPI" {
  name        = "comics_api"
  description = "API to access autocompletion comics"
}

resource "aws_api_gateway_resource" "api_resource" {
  rest_api_id = aws_api_gateway_rest_api.comicsAPI.id
  parent_id   = aws_api_gateway_rest_api.comicsAPI.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "api_method" {
  rest_api_id   = aws_api_gateway_rest_api.comicsAPI.id
  resource_id   = aws_api_gateway_resource.api_resource.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "comicsAPIIntegration" {
  rest_api_id = aws_api_gateway_rest_api.comicsAPI.id
  resource_id = aws_api_gateway_rest_api.comicsAPI.root_resource_id
  http_method = "ANY"
  type        = "AWS_PROXY"
  uri         = aws_lambda_function.autocompletion_comics_lambda.invoke_arn
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.autocompletion_comics_lambda.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.comicsAPI.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "api_deployment" {
  depends_on = [aws_api_gateway_integration.comicsAPIIntegration]

  rest_api_id = aws_api_gateway_rest_api.comicsAPI.id
  stage_name  = "test"
}
