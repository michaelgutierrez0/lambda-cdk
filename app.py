#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import App, Tags, Environment
from lambda_cdk.lambda_cdk_stack import LambdaCdkStack


app = App()
lambda_cdk_stack = LambdaCdkStack(
    app,
    "LambdaCdkStack",
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

# Add tags to stack
Tags.of(lambda_cdk_stack).add("name", "Michael Gutierrez")
Tags.of(lambda_cdk_stack).add("owner", "mwgutier@gmail.com")

app.synth()
