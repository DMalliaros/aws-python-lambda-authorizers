#!/usr/bin/env python3
import os
from aws_cdk import App, Environment
from aws_python_lambda_authorizers_stack import AwsPythonLambdaAuthorizersStack

app = App()

AwsPythonLambdaAuthorizersStack(
    app,
    "AwsPythonLambdaAuthorizersStack",
    env=Environment(
        account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
        region=os.environ.get("CDK_DEFAULT_REGION"),
    ),
)

app.synth()
