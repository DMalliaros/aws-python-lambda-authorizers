import unittest

from src.util.method_arn_util import MethodArnUtil


class TestMethodArn(unittest.TestCase):
    def test_init__should_return_structure_method_arn_object__when_everything_is_ok(self):
        method_arn_str = "arn:aws:execute-api:<Region id>:<Account id>:<API id>/<Stage>/<Method>/<Resource path>"

        method_arn = MethodArnUtil(method_arn_str)

        self.assert_method_arn(method_arn)
        self.assertEqual("<Method>", method_arn.method)
        self.assertEqual("/<Resource path>", method_arn.resource)

    def test_init__should_return_structure_method_arn_object__when_resource_path_has_sub_path(self):
        method_arn_str = "arn:aws:execute-api:<Region id>:<Account id>:<API id>/<Stage>/<Method>/<Resource path>/<Sub path>"

        method_arn = MethodArnUtil(method_arn_str)

        self.assert_method_arn(method_arn)
        self.assertEqual("<Method>", method_arn.method)
        self.assertEqual("/<Resource path>/<Sub path>", method_arn.resource)

    def test_init__should_return_structure_method_arn_object__when_resource_is_root(self):
        method_arn_str = "arn:aws:execute-api:<Region id>:<Account id>:<API id>/<Stage>/<Method>/"

        method_arn = MethodArnUtil(method_arn_str)

        self.assert_method_arn(method_arn)
        self.assertEqual("<Method>", method_arn.method)
        self.assertEqual("/", method_arn.resource)

    def assert_method_arn(self, method_arn):
        self.assertEqual("<Region id>", method_arn.region)
        self.assertEqual("<Account id>", method_arn.aws_account_id)
        self.assertEqual("<API id>", method_arn.rest_api_id)
        self.assertEqual("<Stage>", method_arn.stage)
        self.assertEqual("<Method>", method_arn.method)


if __name__ == '__main__':
    unittest.main()
