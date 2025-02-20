import os

import aws_cdk as cdk
from aws_cdk import (
    Stack)
from aws_cdk import aws_lambda as _lambda
from constructs import Construct


class RtbfNewsScraperAwsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        urls_lambda = _lambda.DockerImageFunction(
            self, "GetUrlsSitemap",
            memory_size=2048,
            code=_lambda.DockerImageCode.from_image_asset(
                directory=os.path.join(os.path.dirname(__file__), "../lambda/urls-check")),
            timeout=cdk.Duration.minutes(15)
        )
        cdk.CfnOutput(self, "LambdaFunctionArn", value=urls_lambda.function_arn)
