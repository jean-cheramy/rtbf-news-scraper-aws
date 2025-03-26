import aws_cdk as cdk
from aws_cdk import (
    aws_dynamodb as dynamodb,
)

articles_table_data = {"name": "RTBFArticles",
                      "partition_key": "url",
                      "sort_key": "date",
                       "read_capacity": 20,
                       "write_capacity": 20}

def create_dynamodb_table(scope, table_data):
    return dynamodb.Table(
        scope,
        table_data["name"],
        partition_key=dynamodb.Attribute(
            name=table_data["partition_key"],
            type=dynamodb.AttributeType.STRING
        ),
        sort_key=dynamodb.Attribute(
            name=table_data["sort_key"],
            type=dynamodb.AttributeType.STRING
        ),
        removal_policy=cdk.RemovalPolicy.DESTROY,
        billing_mode=dynamodb.BillingMode.PROVISIONED,
        read_capacity=table_data["read_capacity"],
        write_capacity=table_data["write_capacity"],
    )
