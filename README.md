# Amazon API Gateway Lambda Authorizer & Cognito User Pool
##### com.dmalliaros.aws.lambda_authorizer
**Event**

The event that the lambda authorizer expect have the following format. More info you can find on the [link](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html)

```json
{
    "type": "TOKEN",
    "methodArn": "arn:aws:execute-api:{regionId}:{accountId}:{apiId}/{stage}/{httpVerb}/{resource}",
    "authorizationToken": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciO......"
}
```
**Cognito Bearer Token**

The Cognito the token that creates have the following format

```json
{
   "at_hash":"123123",
   "sub":"98cfee32-3adc-11ea-81ed-9cb70d06741b",
   "cognito:groups":[
      "admin"
   ],
   "iss":"https://cognito-idp.{regionId}.amazonaws.com/{userpoolID}",
   "cognito:username":"test@klarna.com",
   "nonce":"n-0S6_WzA2Mj",
   "aud":"qwertuiop123654789",
   "token_use":"id",
   "auth_time":1579449466.12106,
   "exp":1579456666.121044,
   "iat":1579449466.12106,
   "email":"test@test.com"
}
```
### Verifying a JSON Web Token 

* Confirm the Structure of the JWT 
* Validate the JWT Signature
    * Get public JSON Web Keys (JWK) 
    
        `ex.: https://cognito-idp.{regionId}.amazonaws.com/{userpoolID}/.well-known/jwks.json`
    * Find the find based on `kid` in  JWK and on the JWT token
* Verify the Claims 
    * The audience (aud) claim should match the app client ID created in the Amazon Cognito user pool.  
    * Verify that the token is not expired.
    * The issuer (iss) claim should match your user pool.
    
         `ex.: https://cognito-idp.{regionId}.amazonaws.com/{userpoolID}`

More info you can find on the [link](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-verifying-a-jwt.html)


### Lambda Authorizer Output for an Amazon API Gateway 

Amazon API Gateway expect the following format. More info you can find on the [link](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-lambda-authorizer-output.html)

```json
{
  "principalId": "yyyyyyyy",
  "policyDocument": {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "execute-api:Invoke",
        "Effect": "Allow|Deny",
        "Resource": "arn:aws:execute-api:{regionId}:{accountId}:{apiId}/{stage}/{httpVerb}/{resource}/{child-resources}"
      }
    ]
  },
  "context": {
    "stringKey": "value",
    "numberKey": "1",
    "booleanKey": "true"
  },
  "usageIdentifierKey": "{api-key}"
}
```

### Deploy

For the deployment I use the serverless framework 
```shell script
sls deploy
```

### Remove All the Stack

with the serverless with the eas way that exist to deploy your stack you can also remove it  

```shell script
sls remove
```