from aws_cdk import (
    Duration,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as sfn_tasks,
)


def define_task(scope, task_data, lambda_function, articles_table):
        return sfn_tasks.LambdaInvoke(
        scope,
        task_data["name"],
        lambda_function=lambda_function,
        retry_on_service_exceptions=True,
        retry=task_data["retry"],
        output_path=task_data["output_path"],
        parameters = {
            "table_name": articles_table.table_name
        }
    )

def define_map(scope, map_data, lambda_function, articles_table):
    map_data["parameters"]["table_name"] = articles_table.table_name
    return sfn.Map(
        scope,
        map_data["name"],
        max_concurrency=map_data["max_concurrency"],
        input_path=map_data["input_path"],
        items_path=map_data["items_path"],
        parameters=map_data["parameters"],
        result_path=map_data["result_path"]
    ).iterator(
        define_task(scope, map_data["iterator"], lambda_function)
    )


get_urls_task_data = {
    "name": "GetUrls",
    "retry": sfn.Retry(
        max_attempts=3,
        interval=Duration.seconds(2),
        backoff_rate=2
    ),
    "output_path": "$.Payload"}

scrape_url_map_data =  {
    "name": "ScrapeUrls",
    "max_concurrency": 3,
    "input_path": "$.urls",
    "items_path": "$",
    "parameters": {
        "url.$": "$",
        "index.$": "$$.Map.Item.Index"
    },
    "result_path": "$.Payload",
    "iterator": {
        "name": "ScrapeUrl",
        "retry": sfn.Retry(
            max_attempts=2,
            interval=Duration.seconds(2),
            backoff_rate=1.5
        ),
        "output_path": "$.Payload"
    }
}

topic_modeling_data = {
    "name": "TopicModeling",
    "retry": sfn.Retry(
        max_attempts=2,
        interval=Duration.seconds(2),
        backoff_rate=1.5
    ),
    "output_path": "$.Payload"
}