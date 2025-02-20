import os

import aws_cdk as cdk
from aws_cdk import (
    Stack)
from aws_cdk import (
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks
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

        # Step Function task to invoke the Lambda function
        get_urls_task = tasks.LambdaInvoke(self, "InvokeLambda",
            lambda_function=urls_lambda,
            result_path="$.lambda_result"  # Store result in state machine context
        )

        # Step Function definition (one step for now)
        definition = get_urls_task

        # Create Step Function
        state_machine = sfn.StateMachine(self, "RTBFScrapingStateMachine",
            definition=definition,
            timeout=cdk.Duration.minutes(15)
        )
