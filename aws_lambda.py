import json

from providers import golem


def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps(golem.get(), indent=4),
    }
