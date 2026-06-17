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
   export USER_POOL_ID=eu-west-1_XXXXXXXX
   export USER_POOL_CLIENT_ID=CLIENT_ID_1,CLIENT_ID_2
   cdk bootstrap -c stackType=both
   ```

## Deploy 

### Cognito stack

To avoid creating and destroying every time the Cognito stack (since it has to do only with the users), we deploy it in a separate stack. Say, if we want to destroy it, we destroy only one of them, or we can destroy both of them. 

```bash
cd cdk
cdk deploy -c stackType=cognito
```

### Authorizer stack

Provide the Cognito values as CDK context:

```bash
cdk deploy -c stackType=authorizer -c userPoolId=eu-west-1_XXXXXXXX -c userPoolClientId=CLIENT_ID_1,CLIENT_ID_2
```

Alternatively, use environment variables:

```bash
export USER_POOL_ID=eu-west-1_XXXXXXXX
export USER_POOL_CLIENT_ID=CLIENT_ID_1,CLIENT_ID_2
cdk deploy -c stackType=authorizer
```

### Deploy both

I can deploy both stacks using the following command: 

```
cdk deploy -c stackType=both
```

### Destroy

Drop both stacks, or it's one individual.

```bash
export USER_POOL_ID=eu-west-1_XXXXXXXX
export USER_POOL_CLIENT_ID=CLIENT_ID_1,CLIENT_ID_2
cdk destroy -c stackType=both
``` 

## Notes

- The API path is `/demo`.
- CORS is enabled for GET and OPTIONS.
- The authorizer Lambda receives `USER_POOL_ID`, `CLIENT_IDS`, and `REGION` in environment variables.
