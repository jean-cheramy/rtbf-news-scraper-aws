# lambda/topic_modeling/index.py
import json
import os
import boto3
from bertopic import BERTopic
import pandas as pd
from typing import List, Dict


def process_batch(articles: List[Dict], model: BERTopic):
    # Extract texts
    texts = [article['content'] for article in articles]

    # Fit the model and get topics
    topics, probs = model.fit_transform(texts)

    # Get topic info
    topic_info = model.get_topic_info()

    return topics, topic_info


def handler(event, context):
    try:
        # Initialize DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ['TABLE_NAME'])
        batch_size = int(os.environ['BATCH_SIZE'])

        # Scan DynamoDB table for articles
        response = table.scan()
        articles = response['Items']

        # Process in batches to manage memory
        model = BERTopic(language="french")

        for i in range(0, len(articles), batch_size):
            batch = articles[i:i + batch_size]
            topics, topic_info = process_batch(batch, model)

            # Update articles with topics
            for j, article in enumerate(batch):
                table.update_item(
                    Key={'url': article['url']},
                    UpdateExpression='SET topics = :t',
                    ExpressionAttributeValues={
                        ':t': topics[j].tolist()
                    }
                )

        return {
            'statusCode': 200,
            'body': 'Topic modeling completed successfully'
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error in topic modeling: {str(e)}'
        }
