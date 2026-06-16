# AWS CDK Python App

This CDK app deploys the existing `authorizerFunc` and `hello` Lambda functions with an API Gateway REST API and a Lambda token authorizer.

## Setup

1. Create a Python virtual environment:

   ```bash
   cd cdk
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Bootstrap the environment if needed:

   ```bash
   cdk bootstrap
   ```

## Deploy

Provide the Cognito values as CDK context:

```bash
cdk deploy -c userPoolId=eu-west-1_XXXXXXXX -c userPoolClientId=CLIENT_ID_1,CLIENT_ID_2
```

Alternatively, use environment variables:

```bash
export USER_POOL_ID=eu-west-1_XXXXXXXX
export USER_POOL_CLIENT_ID=CLIENT_ID_1,CLIENT_ID_2
cdk deploy
```

## Notes

- The API path is `/demo`.
- CORS is enabled for GET and OPTIONS.
- The authorizer Lambda receives `USER_POOL_ID`, `CLIENT_IDS`, and `REGION` in environment variables.
