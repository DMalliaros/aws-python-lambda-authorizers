
class MethodArnUtil:

    api_gateway_arn_str = ""
    aws_account_id = ""
    rest_api_id = ""
    resource = ""
    region = ""
    method = ""
    stage = ""

    def __init__(self, method_arn_str):
        method_arn_parts = method_arn_str.split(':')
        self.aws_account_id = method_arn_parts[4]
        self.region = method_arn_parts[3]
        self.api_gateway_arn_str = method_arn_parts[5]

        api_gateway_arn_parts = self.api_gateway_arn_str.split('/')
        self.rest_api_id = api_gateway_arn_parts[0]
        self.stage = api_gateway_arn_parts[1]
        self.method = api_gateway_arn_parts[2]

        for i in range(3, len(api_gateway_arn_parts)):
            self.resource = self.resource + "/" + api_gateway_arn_parts[i]

