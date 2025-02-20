import os

import aws_cdk as cdk
from aws_cdk import (
    Stack)
from aws_cdk import (
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_iam as iam
)
from constructs import Construct
import aws_cdk as cdk


class RtbfNewsScraperAwsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # Create an S3 bucket
        urls_bucket = s3.Bucket(self, "UrlsBucket",
                           removal_policy=cdk.RemovalPolicy.DESTROY)

        # IAM Role for Lambda to access S3
        urls_lambda_role = iam.Role(self, "LambdaS3Role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
            ]
        )

        urls_lambda = _lambda.DockerImageFunction(
            self, "GetUrlsSitemap",
            memory_size=2048,
            code=_lambda.DockerImageCode.from_image_asset(
                directory=os.path.join(os.path.dirname(__file__), "../lambda/urls-check")),
            timeout=cdk.Duration.minutes(15),
            environment={
                "BUCKET_NAME": urls_bucket.bucket_name,
                "FILE_NAME": "processed_urls.json",
                "RTBF_URL" : "https://www.rtbf.be/site-map/articles5000.xml"
            },
            role=urls_lambda_role
        )
        cdk.CfnOutput(self, "LambdaFunctionArn", value=urls_lambda.function_arn)

        #urls_bucket.grant_write(urls_lambda)
        #urls_bucket.grant_read(urls_lambda)
