from src.models.effect_verb import Effect


class Statement:
    action = "execute-api:Invoke"
    effect = ""
    resource = ""

    def __init__(self, effect, resource):

        if not isinstance(effect, Effect):
            raise Exception("Invalid Effect verb :" + effect + ". Allowed verbs in Effect class")
        self.effect = effect
        self.resource = resource
