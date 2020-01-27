import json

from src.model.policy_document import PolicyDocument


class AuthPolicyResponse:
    principal_id = ""
    context = {}
    policy_document = {}

    def __init__(self, principal_id, policy_document):
        if not isinstance(policy_document, PolicyDocument):
            raise Exception("Invalid PolicyDocument")
        self.principal_id = principal_id
        self.context = {}
        self.policy_document = {
            'Version': policy_document.version,
            'Statement': policy_document.statements
        }

    def add_context(self, key, value):
        self.context[key] = value

    def build_response(self, is_json=False):
        response = {
            'principalId': self.principal_id,
            'policyDocument': self.policy_document,
            'context': self.context
        }
        return response if is_json is False else json.dumps(response)
