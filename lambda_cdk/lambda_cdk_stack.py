from aws_cdk import (
    aws_lambda as _lambda,
    aws_s3 as _s3,
    aws_s3_notifications,
    Stack,
)
from constructs import Construct


class LambdaCdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create lambda function
        s3_lambda_function = _lambda.Function(
            self,
            "lambda_function",
            function_name="lambda_read_s3_object_trigger",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda-handler.lambda_handler",
            code=_lambda.Code.from_asset("./lambda"),
        )
        # create s3 bucket
        s3 = _s3.Bucket(
            self,
            "s3bucket",
            bucket_name="lambda-cdk-s3-bucket-michaelg",
            block_public_access=_s3.BlockPublicAccess.BLOCK_ALL,
            encryption=_s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
            versioned=True,
        )

        # create s3 notification for lambda function
        notification = aws_s3_notifications.LambdaDestination(s3_lambda_function)

        # assign notification for the s3 event type (ex: OBJECT_CREATED)
        s3.add_event_notification(_s3.EventType.OBJECT_CREATED, notification)

        # allow Lambda to read the bucket
        s3.grant_read(s3_lambda_function)
