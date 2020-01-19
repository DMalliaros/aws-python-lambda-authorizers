import unittest

from src.model.effect_verb import Effect
from src.model.policy_document import PolicyDocument
from src.model.statement import Statement


class TestPolicyDocument(unittest.TestCase):
    version = "2012-10-17"

    def test_add_statement__should_return_correct_policy_document__when_everything_is_ok(self):
        """
        should_return_correct_policy_document_with_one_statement
        when_everything_is_ok_and_one_statement_are_pass
        """
        statement = Statement(Effect.ALLOW, "resource")

        policy_document = PolicyDocument()
        policy_document.add_statement(statement)

        self.assertEqual(policy_document.version, self.version)
        self.assertEqual(len(policy_document.statements), 1)
        self._assert_statement_of_policy_document(policy_document.statements[0], statement)

    def test_add_statement__should_return_correct_policy_document__when_everything_is_ok02(self):
        """
        should_return_correct_policy_document_with_more_that_one_statement
        when_everything_is_ok_and_more_than_one_statement_are_pass
        """
        statement0 = Statement(Effect.ALLOW, "resource/1")
        statement1 = Statement(Effect.ALLOW, "resource/2")

        policy_document = PolicyDocument()
        policy_document.add_statement(statement0)
        policy_document.add_statement(statement1)

        self.assertEqual(policy_document.version, self.version)
        self.assertEqual(2, len(policy_document.statements))
        self._assert_statement_of_policy_document(policy_document.statements[0], statement0)
        self._assert_statement_of_policy_document(policy_document.statements[1], statement1)

    def test_add_statement__should_throw_exception__when_effect_is_not_statement_class(self):
        """
        should_throw_exception
        when_effect_is_not_statement_class
        """
        statement = {
            "action": "",
            "effect": Effect.ALLOW,
            "resource": "resource"
        }
        policy_document = PolicyDocument()
        with self.assertRaises(Exception) as context:
            policy_document.add_statement(statement)
            self.fail("Expect NameError")

        self.assertEqual(context.exception.args[0], "Invalid Statement is not class Statement")

    def _assert_statement_of_policy_document(self, policy_document_statements, statement):
        self.assertEqual(policy_document_statements["Action"], statement.action)
        self.assertEqual(policy_document_statements["Effect"], statement.effect.value)
        self.assertEqual(policy_document_statements["Resource"], statement.resource)


if __name__ == '__main__':
    unittest.main()
