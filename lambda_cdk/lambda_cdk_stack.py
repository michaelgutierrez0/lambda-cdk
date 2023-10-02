from aws_cdk import (
    aws_lambda as _lambda,
    aws_s3 as _s3,
    aws_s3_notifications,
    aws_iam as _iam,
    Stack,
    RemovalPolicy,
)
from constructs import Construct
from aws_cdk.aws_iam import Effect


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
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # create bucket policy to only allow Lambda to access the bucket
        s3_policy = _iam.PolicyStatement(
            effect=Effect.DENY,
            resources=[s3.arn_for_objects("*")],
            actions=["s3:*"],
            principals=[_iam.AnyPrincipal()],
        )

        s3_policy.add_condition(
            "StringNotLike",
            {
                "aws:PrincipalArn": [
                    s3_lambda_function.role.role_arn,
                    "arn:aws:iam::262340536653:user/MichaelGutierrez",
                ]
            },
        )

        # apply bucket policy
        s3.add_to_resource_policy(s3_policy)

        # create s3 notification for lambda function
        notification = aws_s3_notifications.LambdaDestination(s3_lambda_function)

        # assign notification for the s3 event type (ex: OBJECT_CREATED)
        s3.add_event_notification(_s3.EventType.OBJECT_CREATED, notification)
