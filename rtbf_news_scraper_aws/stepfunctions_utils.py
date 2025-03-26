from aws_cdk import (
    Duration,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as sfn_tasks,
)


def define_task(scope, task_data, lambda_function, articles_table):
        task = sfn_tasks.LambdaInvoke(
        scope,
        task_data["name"],
        lambda_function=lambda_function,
        retry_on_service_exceptions=True,
        output_path=task_data["output_path"],
        payload=sfn.TaskInput.from_object({
                "table_name": articles_table.table_name
            })
    )
        task.add_retry(
            max_attempts=task_data["retry"]["max_attempts"],
            interval=Duration.seconds(task_data["retry"]["interval"]),
            backoff_rate=task_data["retry"]["backoff_rate"]
        )

        return task

def define_map(scope, map_data, lambda_function, articles_table):
    return sfn.Map(
        scope,
        map_data["name"],
        max_concurrency=map_data["max_concurrency"],
        input_path=map_data["input_path"],
        items_path=map_data["items_path"],
        parameters={
            "url.$": "$",
            "index.$": "$$.Map.Item.Index",
            "table_name": articles_table.table_name
        },
    result_path=map_data["result_path"]
    ).iterator(
        define_task(scope, map_data["iterator"], lambda_function, articles_table)
    )


get_urls_task_data = {
    "name": "GetUrlsTask",
    "retry": {
        "max_attempts": 3,
        "interval": 2,
        "backoff_rate": 2},
    "output_path": "$.Payload"}

scrape_url_map_data =  {
    "name": "ScrapeUrlsMapTask",
    "max_concurrency": 3,
    "input_path": "$.urls",
    "items_path": "$",
    "result_path": "$.Payload",
    "iterator": {
        "name": "ScrapeUrl",
        "retry": {
            "max_attempts": 2,
            "interval": 2,
            "backoff_rate": 1.5},
        "output_path": "$.Payload"
    }
}

topic_modeling_data = {
    "name": "TopicModelingTask",
    "retry": {
        "max_attempts": 2,
        "interval": 2,
        "backoff_rate": 1.5},
    "output_path": "$.Payload"
}