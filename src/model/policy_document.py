from src.model.statement import Statement


class PolicyDocument:
    version = "2012-10-17"
    statements = []

    def __init__(self):
        self.statements = []

    def add_statement(self, statement):
        if not isinstance(statement, Statement):
            raise Exception("Invalid Statement is not class Statement")

        self.statements.append({
            "Action": statement.action,
            "Effect": statement.effect.value,
            "Resource": statement.resource
        })
