from src.models.http_verb import HttpVerb


class ResourceArnUtil:
    _execute_arn_format = "arn:aws:execute-api:{}:{}:{}/{}/{}/{}"
    aws_account_id = ""
    rest_api_id = "*"
    region = "*"
    stage = "*"

    def __init__(self, region, aws_account_id, rest_api_id, stage):
        self.aws_account_id = aws_account_id
        self.rest_api_id = rest_api_id
        self.region = region
        self.stage = stage

    def generate_resource_arn(self, http_method, resource_path):
        if resource_path is None or not resource_path:
            raise Exception("No path provided")
        resource = resource_path[1:] if resource_path.startswith('/') else resource_path
        verb = http_method.upper()
        if not hasattr(HttpVerb, verb):
            raise NameError("Invalid HTTP verb " + verb + ". Allowed verbs in HttpVerb class")

        return self._execute_arn_format.format(
            self.region, self.aws_account_id, self.rest_api_id, self.stage, getattr(HttpVerb, verb), resource)
