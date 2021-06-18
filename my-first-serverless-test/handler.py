import json


def mic_check(event, context):
    body = {
        "message": "Mic check! Checking the mic! 1-2, 1-2! Are my levels good?",
        "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}
