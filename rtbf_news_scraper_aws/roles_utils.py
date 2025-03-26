from aws_cdk import (
    aws_iam as iam
)

get_urls_role_data = {"name": "GetUrlsLambdaRole",
                                              "service": "lambda.amazonaws.com",
                                              "policies": [
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaBasicExecutionRole"),
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        ]}
scrape_url_role_data = {"name": "ScrapeUrlLambdaRole",
                                              "service": "lambda.amazonaws.com",
                                              "policies": [
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaBasicExecutionRole"),
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        ]}
topic_modeling_role_data = {"name": "TopicsModelingLambdaRole",
                                              "service": "lambda.amazonaws.com",
                                              "policies": [
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaBasicExecutionRole"),
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBReadWriteAccess")
        ]}

def build_roles(scope, role_init):
    return iam.Role(scope, role_init["name"],
                    assumed_by=iam.ServicePrincipal(role_init["service"]),
                    managed_policies=role_init["policies"]
                    )
