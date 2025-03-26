import aws_cdk as cdk
from aws_cdk import (
    Stack,
    Duration,
    aws_s3 as s3,
    aws_stepfunctions as sfn
)
from constructs import Construct

from .lambdas_utils import build_lambda_docker, get_urls_lambda_data, scrape_url_lambda_data, topic_modeling_lambda_data
from .dynamodb_table_utils import create_dynamodb_table, articles_table_data
from .roles_utils import build_roles, get_urls_role_data, scrape_url_role_data, topic_modeling_role_data
from .stepfunctions_utils import get_urls_task_data, scrape_url_map_data, topic_modeling_data, define_task, define_map


class RtbfNewsScraperAwsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        urls_bucket = s3.Bucket(self, "UrlsBucket",
                           removal_policy=cdk.RemovalPolicy.DESTROY)
        # -----------------------------------------------
        # ROLES INITIALIZATION
        # -----------------------------------------------
        get_urls_lambda_role = build_roles(self, get_urls_role_data)
        scrape_url_lambda_role = build_roles(self, scrape_url_role_data)
        topic_modeling_lambda_role = build_roles(self, topic_modeling_role_data)

        # -----------------------------------------------
        # DYNAMODB INITIALIZATION
        # -----------------------------------------------
        articles_table = create_dynamodb_table(self, articles_table_data)

        # -----------------------------------------------
        # LAMBDAS INITIALIZATION
        # -----------------------------------------------
        get_urls_lambda = build_lambda_docker(self, get_urls_lambda_data, get_urls_lambda_role, urls_bucket, articles_table)
        scrape_url_function = build_lambda_docker(self, scrape_url_lambda_data, scrape_url_lambda_role, urls_bucket, articles_table)
        topic_modeling_lambda = build_lambda_docker(self, topic_modeling_lambda_data, topic_modeling_lambda_role, None,
                                                    articles_table)

        # -----------------------------------------------
        # GRANTING PERMISSIONS TO LAMBDAS
        # -----------------------------------------------
        articles_table.grant_read_write_data(get_urls_lambda)
        articles_table.grant_read_write_data(topic_modeling_lambda)
        articles_table.grant_write_data(scrape_url_function)

        # -----------------------------------------------
        # STEPFUNCTION TASKS
        # -----------------------------------------------
        get_urls_task = define_task(self, get_urls_task_data, get_urls_lambda, articles_table)
        scrape_urls = define_map(self, scrape_url_map_data, scrape_url_function, articles_table)
        topic_modeling_task = define_task(self, topic_modeling_data, topic_modeling_lambda, articles_table)

        # Build the workflow
        definition = (
            get_urls_task
            .next(
                sfn.Choice(self, "CheckUrls")
                .when(
                    sfn.Condition.is_present("$.urls"),
                    scrape_urls
                    .next(topic_modeling_task)
                )
                .otherwise(
                    sfn.Fail(
                        self,
                        "NoUrlsFound",
                        cause="No URLs were returned",
                        error="EmptyUrlList"
                    )
                )
            )
        )

        state_machine = sfn.StateMachine(
            self,
            "RtbfNewsScraperStateMachine",
            definition=definition,
            timeout=Duration.minutes(30),
            state_machine_type=sfn.StateMachineType.STANDARD,
        )
