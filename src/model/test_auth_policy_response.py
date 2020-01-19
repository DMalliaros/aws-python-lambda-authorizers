import unittest
from src.model.auth_policy_response import AuthPolicyResponse
from src.model.effect_verb import Effect
from src.model.policy_document import PolicyDocument
from src.model.statement import Statement


class TestAuthPolicyResponse(unittest.TestCase):
    principal_id = "user123"
    policy_document = {}

    def setUp(self):
        statement = Statement(Effect.ALLOW, "resource")
        policy_document = PolicyDocument()
        policy_document.add_statement(statement)
        self.policy_document = policy_document

    def test_add_context__should_add_context__when_everything_is_ok(self):
        auth_policy_response = AuthPolicyResponse(self.principal_id, self.policy_document)
        auth_policy_response.add_context("key0", "vale0")
        auth_policy_response.add_context("key1", "vale1")

        self.assertEqual(self.principal_id, auth_policy_response.principal_id)
        self.assertEqual(self.policy_document.version, auth_policy_response.policy_document["Version"])
        self.assertEqual(self.policy_document.statements, auth_policy_response.policy_document["Statement"])
        self.assertEqual("vale0", auth_policy_response.context["key0"])
        self.assertEqual("vale1", auth_policy_response.context["key1"])

    def test_build_response__should_return_correct_auth_policy_response_object__when_everything_is_ok(self):
        auth_policy_response = AuthPolicyResponse(self.principal_id, self.policy_document)
        auth_policy_response.add_context("key0", "vale0")
        response = auth_policy_response.build_response()

        self.assertEqual(auth_policy_response.principal_id, response["principalId"])
        self.assertEqual(auth_policy_response.policy_document, response["policyDocument"])
        self.assertEqual(auth_policy_response.policy_document["Version"], response["policyDocument"]["Version"])
        self.assertEqual(auth_policy_response.policy_document["Statement"], response["policyDocument"]["Statement"])
        self.assertEqual(auth_policy_response.context["key0"], response["context"]["key0"])

    def test_build_response__should_return_correct_auth_policy_response_string__when_everything_is_ok_and_json_are_true(
            self):
        auth_policy_response = AuthPolicyResponse(self.principal_id, self.policy_document)
        response = auth_policy_response.build_response(is_json=True)

        self.assertIn("principalId", response)
        self.assertIn("policyDocument", response)
        self.assertIn("context", response)


if __name__ == '__main__':
    unittest.main()
