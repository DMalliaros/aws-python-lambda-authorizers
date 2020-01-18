import unittest

from src.util.resource_arn_util import ResourceArnUtil


class TestResourceArnUtil(unittest.TestCase):
    aws_account_id = "<Account id>"
    rest_api_id = "<REST API id>"
    region = "<Region id>"
    stage = "<Stage>"

    def test_generate_resource_arn__should_return_correct_arn__when_everything_is_ok_and_path_starts_with_slash(self):
        resource_arn = ResourceArnUtil(self.region, self.aws_account_id, self.rest_api_id, self.stage)
        verb = "GET"
        resource = "/v1/tmp"

        arn = resource_arn.generate_resource_arn(verb, resource)

        self.assertEqual(arn, "arn:aws:execute-api:" +
                         self.region + ":" +
                         self.aws_account_id + ":" +
                         self.rest_api_id + "/" +
                         self.stage + "/" +
                         verb +
                         resource)

    def test_generate_resource_arn__should_return_correct_arn__when_everything_is_ok_and_path_not_starts_with_slash(self):
        resource_arn = ResourceArnUtil(self.region, self.aws_account_id, self.rest_api_id, self.stage)
        verb = "GET"
        resource = "v1/tmp"

        arn = resource_arn.generate_resource_arn(verb, resource)

        self.assertEqual(arn, "arn:aws:execute-api:" +
                         self.region + ":" +
                         self.aws_account_id + ":" +
                         self.rest_api_id + "/" +
                         self.stage + "/" +
                         verb + "/" +
                         resource)

    def test_generate_resource_arn__should_return_correct_arn__when_everything_is_ok_and_path_is_root(self):
        resource_arn = ResourceArnUtil(self.region, self.aws_account_id, self.rest_api_id, self.stage)
        verb = "GET"
        resource = "/"

        arn = resource_arn.generate_resource_arn(verb, resource)

        self.assertEqual(arn, "arn:aws:execute-api:" +
                         self.region + ":" +
                         self.aws_account_id + ":" +
                         self.rest_api_id + "/" +
                         self.stage + "/" +
                         verb + "/")

    def test_generate_resource_arn__should_throw_error__when_path_is_empty(self):
        resource_arn = ResourceArnUtil(self.region, self.aws_account_id, self.rest_api_id, self.stage)
        verb = "GET"
        resource = ""

        with self.assertRaises(Exception) as context:
            resource_arn.generate_resource_arn(verb, resource)
            self.fail("Expect NameError")

        self.assertEqual(context.exception.args[0], 'No path provided')

    def test_generate_resource_arn__should_throw_error__when_path_is_none(self):
        resource_arn = ResourceArnUtil(self.region, self.aws_account_id, self.rest_api_id, self.stage)
        verb = "GET"
        resource = None

        with self.assertRaises(Exception) as context:
            resource_arn.generate_resource_arn(verb, resource)
            self.fail("Expect NameError")

        self.assertEqual(context.exception.args[0], 'No path provided')

    def test_generate_resource_arn__should_throw_name_error__when_http_verb_not_much(self):
        resource_arn = ResourceArnUtil(self.region, self.aws_account_id, self.rest_api_id, self.stage)
        verb = "GET00"
        resource = "v1/tmp"

        with self.assertRaises(NameError) as context:
            resource_arn.generate_resource_arn(verb, resource)
            self.fail("Expect NameError")

        self.assertEqual(context.exception.args[0],
                         'Invalid HTTP verb {}. Allowed verbs in HttpVerb class'.format(verb))

    def test_generate_resource_arn__should_return_correct_arn__when_everything_is_ok_and_verb_is_lower_case(self):
        resource_arn = ResourceArnUtil(self.region, self.aws_account_id, self.rest_api_id, self.stage)
        verb = "get"
        resource = "/v1/tmp"

        arn = resource_arn.generate_resource_arn(verb, resource)

        self.assertEqual(arn, "arn:aws:execute-api:" +
                         self.region + ":" +
                         self.aws_account_id + ":" +
                         self.rest_api_id + "/" +
                         self.stage + "/" +
                         "GET" +
                         resource)

    def test_generate_resource_arn__should_return_correct_arn__when_everything_is_ok_and_verb_is_all(self):
        resource_arn = ResourceArnUtil(self.region, self.aws_account_id, self.rest_api_id, self.stage)
        verb = "ALL"
        resource = "/v1/tmp"

        arn = resource_arn.generate_resource_arn(verb, resource)

        self.assertEqual(arn, "arn:aws:execute-api:" +
                         self.region + ":" +
                         self.aws_account_id + ":" +
                         self.rest_api_id + "/" +
                         self.stage + "/" +
                         "*" +
                         resource)


if __name__ == '__main__':
    unittest.main()
