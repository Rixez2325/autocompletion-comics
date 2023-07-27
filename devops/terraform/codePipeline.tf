resource "aws_codepipeline" "codepipeline" {
  name     = "comics-generator"
  role_arn = "arn:aws:iam::252335110145:role/service-role/AWSCodePipelineServiceRole-eu-west-1-comics-generator"

  artifact_store {
    location = data.aws_s3_bucket.existing.bucket
    type     = "S3"
  }

  stage {
    name = "Source"

    action {
      name             = "Source"
      category         = "Source"
      owner            = "ThirdParty"
      provider         = "GitHub"
      version          = "1"
      output_artifacts = ["source_output"]

      configuration = {
        Owner      = "Rixez2325"
        Repo       = "autocompletion-comics"
        Branch     = "main"
        OAuthToken = "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"
      }
    }
  }

  stage {
    name = "Build"

    action {
      name             = "Build"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      input_artifacts  = ["source_output"]
      output_artifacts = ["build_output"]
      version          = "1"

      configuration = {
        ProjectName = "commics-generator-terraform"
      }
    }
  }
}
