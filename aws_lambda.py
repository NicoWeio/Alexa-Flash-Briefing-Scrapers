import json

from providers import golem


def lambda_handler(event, context):
    golemplus = None
    if event['requestContext']['http']['path'] == "/golem/plus":
        golemplus = True
    if event['requestContext']['http']['path'] == "/golem/nonplus":
        golemplus = False

    return {
        "statusCode": 200,
        "body": json.dumps(golem.get(golemplus), indent=4),
    }
