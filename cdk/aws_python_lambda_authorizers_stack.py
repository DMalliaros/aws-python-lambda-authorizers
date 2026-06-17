import os
from pathlib import Path
from constructs import Construct
from aws_cdk import (
    Stack,
    Aws,
    CfnOutput,
    Duration,
    aws_apigateway as apigateway,
    aws_lambda as _lambda,
)


class AwsPythonLambdaAuthorizersStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        user_pool_id = self.node.try_get_context("userPoolId") or os.getenv("USER_POOL_ID")
        client_ids = self.node.try_get_context("userPoolClientId") or os.getenv("USER_POOL_CLIENT_ID")

        if not user_pool_id or not client_ids:
            raise ValueError(
                "Must provide userPoolId and userPoolClientId via CDK context (-c) or environment variables. "
                "Example: cdk deploy -c userPoolId=eu-west-1_XXXXXXXX -c userPoolClientId=xxxxxxxxxxxxxxxxxxxxxxxx"
            )

        project_root = Path(__file__).resolve().parent.parent

        authorizer_function = _lambda.Function(
            self,
            "AuthorizerFunction",
            runtime=_lambda.Runtime.PYTHON_3_14,
            handler="authorizer.lambda_handler",
            code=_lambda.Code.from_asset(
                str(project_root / "src"),
                exclude=[
                    "**/__pycache__/**",
                    "**/*.pyc",
                ],
            ),
            memory_size=256,
            environment={
                "USER_POOL_ID": user_pool_id,
                "CLIENT_IDS": client_ids,
                "REGION": Aws.REGION,
            },
        )

        hello_function = _lambda.Function(
            self,
            "HelloFunction",
            runtime=_lambda.Runtime.PYTHON_3_14,
            handler="handler.hello",
            code=_lambda.Code.from_asset(
                str(project_root / "demo"),
                exclude=[
                    "**/__pycache__/**",
                    "**/*.pyc",
                ],
            ),
        )

        authorizer = apigateway.TokenAuthorizer(
            self,
            "LambdaTokenAuthorizer",
            handler=authorizer_function,
            identity_source="method.request.header.Authorization",
            results_cache_ttl=Duration.seconds(0),
        )

        api = apigateway.RestApi(
            self,
            "DemoApi",
            rest_api_name="DemoApi",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=["GET", "OPTIONS"],
            ),
        )

        demo_resource = api.root.add_resource("demo")
        demo_resource.add_method(
            "GET",
            apigateway.LambdaIntegration(hello_function),
            authorizer=authorizer,
            authorization_type=apigateway.AuthorizationType.CUSTOM,
        )

        CfnOutput(
            self,
            "ApiUrl",
            value=api.url,
            description="Base URL for the demo API",
        )
