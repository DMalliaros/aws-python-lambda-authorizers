import unittest
import requests_mock

from src.jwks import get_jwks


class TestJWKs(unittest.TestCase):
    issuer_url = "https://cognito-idp.region.amazonaws.com/userPoolId"
    kid = "Key Type (kty)"

    def test_get_jwks__should_return_map_of_keys__when_everything_is_ok(self):
        with requests_mock.Mocker() as mock:
            json_body = {
                "keys": [
                    {
                        "alg": "RS256",
                        "e": "AQAB",
                        "kid": self.kid,
                        "kty": "RSA",
                        "n": "RSA Modulus (n)",
                        "use": "sig"
                    }
                ]
            }
            mock.get(self.issuer_url + '/.well-known/jwks.json', json=json_body,
                     status_code=200)
            response = get_jwks(self.issuer_url)

            self.assertEqual(len(response), 1)
            self.assertTrue(response[self.kid] is not None)
            self.assertEqual(response[self.kid]["alg"], "RS256")
            self.assertEqual(response[self.kid]["e"], "AQAB")
            self.assertEqual(response[self.kid]["kty"], "RSA", )
            self.assertEqual(response[self.kid]["use"], "sig")
            self.assertEqual(response[self.kid]["kid"], self.kid)

    def test_get_jwks__should_throw_exception__when_http_was_not_successful(self):
        with requests_mock.Mocker() as mock:
            keys_url = self.issuer_url + '/.well-known/jwks.json'
            mock.get(keys_url,
                     json={'error': 'not found'}, status_code=404)

            with self.assertRaises(Exception) as context:
                get_jwks(self.issuer_url)
                self.fail("Expect Exception")

            self.assertEqual(context.exception.args[0], 'Http request to cognito jwks url: {} failed'.format(keys_url))


if __name__ == '__main__':
    unittest.main()
