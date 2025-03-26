import os

import aws_cdk as cdk
from aws_cdk import (
    aws_lambda as lambda_
)
from aws_cdk.aws_dynamodb import Table
from aws_cdk.aws_iam import Role
from aws_cdk.aws_s3 import Bucket


def build_lambda_docker(
        scope: cdk.Construct,
        lambda_data: dict,
        role: Role,
        urls_bucket: Bucket | None = None,
        articles_table: Table | None = None
) -> lambda_.DockerImageFunction:
    """
    Creates a Docker-based Lambda function with optional S3 bucket and DynamoDB table.

    :param scope: CDK construct scope.
    :param lambda_data: Dictionary containing lambda configuration.
    :param role: IAM role for the lambda function.
    :param urls_bucket: Optional S3 bucket for storing URLs.
    :param articles_table: Optional DynamoDB table for storing articles.
    :return: DockerImageFunction instance.
    """
    environment = lambda_data.get("environment", {})

    if urls_bucket:
        environment["BUCKET_NAME"] = urls_bucket.bucket_name
    if articles_table:
        environment["TABLE_NAME"] = articles_table.table_name

    return lambda_.DockerImageFunction(
        scope,
        lambda_data["name"],
        memory_size=lambda_data["memory"],
        code=lambda_.DockerImageCode.from_image_asset(
            directory=os.path.join(os.path.dirname(__file__), lambda_data["path"])
        ),
        timeout=cdk.Duration.minutes(lambda_data["timeout"]),
        environment=environment,
        role=role
    )


get_urls_lambda_data = {"name": "GetUrlsSitemap",
                    "memory": 2048,
                    "path": "../lambda/urls-check",
                    "timeout": 15,
                    "environment": {
                        "FILE_NAME": "processed_urls.json",
                        "RTBF_URL": "https://www.rtbf.be/site-map/articles5000.xml"
                    }
                    }

scrape_url_lambda_data = {"name": "ScrapeUrl",
                          "memory": 512,
                          "path": "../lambda/scrape-url",
                          "timeout": 1,
                          "environment": {
                              "FILE_NAME": "processed_urls.json",
                              "RTBF_URL": "https://www.rtbf.be/site-map/articles5000.xml"
                          }
                          }

topic_modeling_lambda_data = {"name": "TopicModeling",
                              "memory": 10240,
                              "path": "../lambda/topic_modeling",
                              "timeout": 15,
                              "environment": {
                                  "BATCH_SIZE": "10"
                              }
                              }
