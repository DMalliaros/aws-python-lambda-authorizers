#!/usr/bin/env python3
import os
from aws_cdk import App, Environment
from aws_python_lambda_authorizers_stack import AwsPythonLambdaAuthorizersStack
from cognito_stack import CognitoStack

app = App()

env = Environment(
    account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
    region=os.environ.get("CDK_DEFAULT_REGION"),
)

# Determine which stack(s) to deploy
# Can be set via environment variable STACK_TYPE or CDK context
# Options: "authorizer", "cognito", or "both"
stack_type = os.environ.get("STACK_TYPE", app.node.try_get_context("stackType") or "authorizer")

if stack_type.lower() in ("authorizer", "both"):
    AwsPythonLambdaAuthorizersStack(
        app,
        "AwsPythonLambdaAuthorizersStack",
        env=env,
    )

if stack_type.lower() in ("cognito", "both"):
    CognitoStack(
        app,
        "DemoCognito",
        env=env,
    )

app.synth()
