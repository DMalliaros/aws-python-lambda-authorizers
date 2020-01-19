import unittest

from src.model.effect_verb import Effect
from src.model.http_verb import HttpVerb
from src.util.resource_arn_util import ResourceArnUtil
from src.model.statement import Statement


class TestStatement(unittest.TestCase):
    resource_arn = ""

    def setUp(self):
        resource_arn_util = ResourceArnUtil("<Region id>", "<Account id>", "<REST API id>", "<Stage>")
        self.resource_arn = resource_arn_util.generate_resource_arn(HttpVerb.GET, "/v1/tmp")

    def test_inti__should_return_correct_statement__when_everything_is_ok(self):
        effect = Effect.ALLOW
        statement = Statement(effect, self.resource_arn)

        self.assertEqual(statement.action, "execute-api:Invoke")
        self.assertEqual(statement.effect, effect)
        self.assertEqual(statement.resource, self.resource_arn)

    def test_inti__should_throw_exception__when_effect_is_not_enum(self):
        effect = "ALLOW"

        with self.assertRaises(Exception) as context:
            Statement(effect, self.resource_arn)
            self.fail("Expect NameError")

        self.assertEqual(context.exception.args[0],
                         "Invalid Effect verb :" + effect + ". Allowed verbs in Effect class")


if __name__ == '__main__':
    unittest.main()
