import os
from constructs import Construct
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_cognito as cognito,
    Tags,
)


class CognitoStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        env = os.getenv("ENVIRONMENT", "demo")
        cognito_domain = os.getenv("COGNITO_DOMAIN", f"{env}user-pool-domain-123")

        callback_urls = os.getenv("COGNITO_CALLBACK_URLS", "http://localhost:3000/")
        logout_urls = os.getenv("COGNITO_LOGOUT_URLS", "http://localhost:3000/")

        callback_url_list = [url.strip() for url in callback_urls.split(",") if url.strip()]
        logout_url_list = [url.strip() for url in logout_urls.split(",") if url.strip()]

        # Add tags
        Tags.of(self).add("environment", env)

        # Create User Pool
        user_pool = cognito.CfnUserPool(
            self,
            f"{construct_id}UserPool",
            user_pool_name=f"{env}-user-pool",
            username_attributes=["email"],
            mfa_configuration="OFF",
            admin_create_user_config=cognito.CfnUserPool.AdminCreateUserConfigProperty(
                allow_admin_create_user_only=True,
            ),
            policies=cognito.CfnUserPool.PoliciesProperty(
                password_policy=cognito.CfnUserPool.PasswordPolicyProperty(
                    minimum_length=6,
                    require_lowercase=False,
                    require_numbers=False,
                    require_symbols=False,
                    require_uppercase=False,
                )
            ),
            user_pool_tags={"environment": env},
        )

        # Create User Pool Client
        user_pool_client = cognito.CfnUserPoolClient(
            self,
            f"{construct_id}UserPoolClient",
            client_name=f"{env}userPoolClient",
            user_pool_id=user_pool.ref,
            generate_secret=False,
            callback_ur_ls=callback_url_list,
            logout_ur_ls=logout_url_list,
            supported_identity_providers=["COGNITO"],
            allowed_o_auth_flows=["implicit"],
            allowed_o_auth_scopes=[
                "aws.cognito.signin.user.admin",
                "email",
                "openid",
            ],
        )

        # Create User Pool Domain
        user_pool_domain = cognito.CfnUserPoolDomain(
            self,
            f"{construct_id}UserPoolDomain",
            domain=cognito_domain,
            user_pool_id=user_pool.ref,
        )

        # Outputs
        CfnOutput(
            self,
            f"{construct_id}OutputUserPoolId",
            description="This is the user pool id",
            export_name="UserPoolId",
            value=user_pool.ref,
        )

        CfnOutput(
            self,
            f"{construct_id}OutputUserPoolURLPrefix",
            description="This is the user pool url Prefix",
            export_name="UserPoolURLPrefix",
            value=user_pool_domain.domain,
        )

        region = self.region
        CfnOutput(
            self,
            f"{construct_id}OutputUserPoolURL",
            description="This is the user pool url",
            export_name="UserPoolURL",
            value=f"https://{user_pool_domain.domain}.auth.{region}.amazoncognito.com",
        )

        CfnOutput(
            self,
            f"{construct_id}OutputUserPoolClientId",
            description="This is the user pool Client id",
            export_name="UserPoolClientId",
            value=user_pool_client.ref,
        )
