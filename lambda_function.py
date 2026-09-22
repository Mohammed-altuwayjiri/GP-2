import json
import boto3
import uuid
from analysis import analyze_review

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('feedback-883425316561-opinion-ai')


def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        review = body.get("review")

        if not review:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Review is required"})
            }

        # ✅ Run your AI model
        result = analyze_review(review)

        category = result["category"]
        opinion = result["opinion"]

        # ✅ Save to DynamoDB
        table.put_item(Item={
            "id": str(uuid.uuid4()),
            "review": review,
            "category": category,
            "opinion": opinion
        })

        return {
            "statusCode": 200,
            "body": json.dumps({
                "review": review,
                "category": category,
                "opinion": opinion
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
