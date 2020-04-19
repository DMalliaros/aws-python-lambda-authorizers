import json
import os
import jwt
import unittest
import uuid
from unittest.mock import patch
from Crypto.PublicKey import RSA
from datetime import datetime, timedelta

from jwt.utils import force_unicode, to_base64url_uint

from src.authorizer import lambda_handler


def build_event_set(token):
    return {
        "type": "TOKEN",
        "methodArn": "arn:aws:execute-api:eu-west-1:111111111111:qwert12345/dev/GET/v1/jobs",
        "authorizationToken": "Bearer " + token
    }


def build_response_jwks_set(kid, modulus, exponent):
    return {
        kid:
            {
                "alg": "RS256", "e": exponent, "kid": kid, "kty": "RSA",
                "use": "sig",
                "n": modulus
            }
    }


def build_claims(sub, case_study):
    after_one_hours_from_now = datetime.now() + timedelta(hours=1)
    before_one_hours_from_now = datetime.now() - timedelta(hours=1)
    return {
        "at_hash": "123123",
        "sub": sub,
        "cognito:groups": [
            "admin"
        ],
        "iss": "https://test.com" if case_study == "different_issuer" else "https://cognito-idp.eu-west-1.amazonaws.com/eu-west-1_abcde1234",
        "cognito:username": "test@klarna.com",
        "nonce": "n-0S6_WzA2Mj",
        "aud": "123123" if case_study == "different_audience" else "qwertuiop123654789",
        "token_use": "id",
        "auth_time": before_one_hours_from_now.timestamp(),
        "exp": before_one_hours_from_now.timestamp() if case_study == "token_expired" else after_one_hours_from_now.timestamp(),
        "iat": before_one_hours_from_now.timestamp(),
        "email": "test@test.com"
    }


class TestAuthorizer(unittest.TestCase):
    kid = "11233112233="
    private_key = ""
    private_key_2 = ""
    exponent = ""
    modulus = ""
    sub = ""

    def setUp(self):
        key = RSA.generate(2048)
        key_2 = RSA.generate(2048)
        self.private_key = key.exportKey().decode("utf-8")
        self.private_key_2 = key_2.exportKey().decode("utf-8")
        self.exponent = force_unicode(to_base64url_uint(key.e))
        self.modulus = force_unicode(to_base64url_uint(key.n))
        self.sub = str(uuid.uuid1())
        os.environ["USER_POOL_ID"] = "eu-west-1_abcde1234"
        os.environ["CLIENT_IDS"] = "qwertuiop123654789"
        os.environ["REGION"] = "eu-west-1"

    @patch("src.authorizer.get_jwks")
    def test_lambda_handler__should_return_policy_with_accept__when_everything_is_ok(self, mock_get_jwks):
        mock_get_jwks.return_value = build_response_jwks_set(self.kid, self.modulus, self.exponent)
        build_claims_content = build_claims(self.sub, "")
        token = jwt.encode(build_claims_content, self.private_key, algorithm='RS256', headers={"kid": self.kid})
        event = build_event_set(token.decode("utf-8"))

        data = lambda_handler(event, None)
        self.assertEqual(self.sub, data["principalId"])
        self.assertEqual(2, len(data["context"]))
        self.assertEqual(build_claims_content["cognito:username"], data["context"]["cognito:username"])
        self.assertEqual(build_claims_content["exp"], data["context"]["exp"])
        self.assertEqual("2012-10-17", data["policyDocument"]["Version"])
        self.assertEqual(1, len(data["policyDocument"]["Statement"]))
        self.assertEqual("Allow", data["policyDocument"]["Statement"][0]["Effect"])
        self.assertEqual("execute-api:Invoke", data["policyDocument"]["Statement"][0]["Action"])
        self.assertEqual("arn:aws:execute-api:eu-west-1:111111111111:qwert12345/dev/*/*",
                         data["policyDocument"]["Statement"][0]["Resource"])

    @patch("src.authorizer.get_jwks")
    def test_lambda_handler__should_return_unauthorized__when_token_expired(self, mock_get_jwks):
        mock_get_jwks.return_value = build_response_jwks_set(self.kid, self.modulus, self.exponent)
        token = jwt.encode(build_claims(self.sub, "token_expired"), self.private_key, algorithm='RS256',
                           headers={"kid": self.kid})
        event = build_event_set(token.decode("utf-8"))

        with self.assertRaises(Exception) as context:
            lambda_handler(event, None)
            self.fail("Expect Exception")

        self.assertEqual(context.exception.args[0], 'Unauthorized')

    @patch("src.authorizer.get_jwks")
    def test_lambda_handler__should_return_unauthorized__when_token_has_different_audience(self, mock_get_jwks):
        mock_get_jwks.return_value = build_response_jwks_set(self.kid, self.modulus, self.exponent)
        token = jwt.encode(build_claims(self.sub, "different_audience"), self.private_key, algorithm='RS256',
                           headers={"kid": self.kid})
        event = build_event_set(token.decode("utf-8"))

        with self.assertRaises(Exception) as context:
            lambda_handler(event, None)
            self.fail("Expect Exception")

        self.assertEqual(context.exception.args[0], 'Unauthorized')

    @patch("src.authorizer.get_jwks")
    def test_lambda_handler__should_return_unauthorized__when_token_has_different_issuer(self, mock_get_jwks):
        mock_get_jwks.return_value = build_response_jwks_set(self.kid, self.modulus, self.exponent)
        token = jwt.encode(build_claims(self.sub, "different_issuer"), self.private_key, algorithm='RS256',
                           headers={"kid": self.kid})
        event = build_event_set(token.decode("utf-8"))

        with self.assertRaises(Exception) as context:
            lambda_handler(event, None)
            self.fail("Expect Exception")

        self.assertEqual(context.exception.args[0], 'Unauthorized')

    @patch("src.authorizer.get_jwks")
    def test_lambda_handler__should_return_unauthorized__when_rsa_not_much(self, mock_get_jwks):
        mock_get_jwks.return_value = build_response_jwks_set(self.kid, self.modulus, self.exponent)
        token = jwt.encode(build_claims(self.sub, ""), self.private_key_2, algorithm='RS256',
                           headers={"kid": self.kid})
        event = build_event_set(token.decode("utf-8"))

        with self.assertRaises(Exception) as context:
            lambda_handler(event, None)
            self.fail("Expect Exception")

        self.assertEqual(context.exception.args[0], 'Unauthorized')


if __name__ == '__main__':
    unittest.main()
