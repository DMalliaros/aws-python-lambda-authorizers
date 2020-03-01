import json

import jwt
import logging
from jwt.algorithms import RSAAlgorithm

from src.jwks import get_jwks
from src.model.auth_policy_response import AuthPolicyResponse
from src.model.effect_verb import Effect
from src.model.http_verb import HttpVerb
from src.model.policy_document import PolicyDocument
from src.model.statement import Statement
from src.util.method_arn_util import MethodArnUtil
from src.environment_parameters import EnvironmentParameters
from src.util.resource_arn_util import ResourceArnUtil


def lambda_handler(event, context):
    environment_parameters = EnvironmentParameters()
    token = event['authorizationToken'].split(' ')[1]
    method_arn_str = event['methodArn']

    claims = jwt.decode(token, verify=False)

    try:
        _assert_issuer_match_user_pool(environment_parameters.issuer_url, claims)
        _assert_signature_is_valid(token, environment_parameters)

    except Exception as e:
        logging.info(e)
        raise Exception('Unauthorized')

    method_arn_util = MethodArnUtil(method_arn_str)
    auth_policy_response = _build_auth_policy(claims, method_arn_util)
    return auth_policy_response.build_response()


def _assert_issuer_match_user_pool(issuer_url, claims):
    iss = claims['iss']
    if issuer_url != iss:
        raise Exception('Token {} not match user pool {}'.format(iss, issuer_url))


def _assert_signature_is_valid(token, environment_parameters):
    public_keys = get_jwks(environment_parameters.issuer_url)
    headers = jwt.get_unverified_header(token)

    kid = headers['kid']
    if kid not in public_keys:
        raise Exception('No public kid {} in JWK set    '.format(kid))

    public_key = RSAAlgorithm.from_jwk(json.dumps(public_keys[kid]))
    jwt.decode(token, public_key, algorithms='RS256', audience=environment_parameters.client_ids,
               issuer=environment_parameters.issuer_url)


def _build_auth_policy(claims, method_arn_util):
    principal_id = claims["sub"]
    policy_document = PolicyDocument()
    auth_policy_response = AuthPolicyResponse(principal_id, policy_document)

    resource_arn_util = ResourceArnUtil(method_arn_util.region, method_arn_util.aws_account_id,
                                        method_arn_util.rest_api_id, method_arn_util.stage)

    resource_arn = resource_arn_util.generate_resource_arn(HttpVerb.ALL, "*")
    statement = Statement(Effect.ALLOW, resource_arn)

    policy_document.add_statement(statement)

    auth_policy_response.add_context("cognito:username", claims["cognito:username"])
    auth_policy_response.add_context("exp", claims["exp"])

    return auth_policy_response
