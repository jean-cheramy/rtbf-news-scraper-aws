# roles_utils.py
from aws_cdk import aws_iam as iam
from aws_cdk import Stack


def build_roles(scope: Stack, role_data: dict) -> iam.Role:
    print(role_data)
    """
    Build an IAM role with specified permissions.

    Args:
        scope (Stack): The CDK Stack scope
        role_data (dict): Role configuration data. Must include 'name' and 'service'.

    Returns:
        iam.Role: The created IAM role
    """
    # Validate required keys
    required_keys = ["name", "service"]
    for key in required_keys:
        if key not in role_data:
            raise ValueError(f"Missing required key '{key}' in role_data")

    # Ensure policies key exists and is a list
    policies = role_data.get("policies", [])
    if not isinstance(policies, list):
        raise TypeError(f"'policies' must be a list, got {type(policies)}")

    managed_policies = [
        iam.ManagedPolicy.from_aws_managed_policy_name(policy_name)
        for policy_name in policies
    ]

    service_principal = iam.ServicePrincipal(role_data["service"])
    return iam.Role(
        scope=scope,
        id=role_data["name"],
        role_name=role_data["name"].lower(),
        assumed_by=service_principal,
        managed_policies=managed_policies or None,
    )


# Role configurations
get_urls_role_data = {
    "name": "GetUrlsLambdaRole",
    "service": "lambda.amazonaws.com",
    "policies": [
        "service-role/AWSLambdaBasicExecutionRole",
        "AmazonS3FullAccess",
        "AmazonDynamoDBFullAccess"
    ]
}

scrape_url_role_data = {
    "name": "ScrapeUrlLambdaRole",
    "service": "lambda.amazonaws.com",
    "policies": [
        "service-role/AWSLambdaBasicExecutionRole",
        "AmazonDynamoDBFullAccess"
    ]
}

topic_modeling_role_data = {
    "name": "TopicModelingLambdaRole",
    "service": "lambda.amazonaws.com",
    "policies": [
        "service-role/AWSLambdaBasicExecutionRole",
        "AmazonDynamoDBFullAccess"
    ]
}
