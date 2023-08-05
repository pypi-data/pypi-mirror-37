from .validator import Validator


class ValidatorFactory():
    asserts = {}

    @classmethod
    def create(cls, types):
        asserts = [cls.getAssert(type) for type in types]

        return Validator(asserts)

    @classmethod
    def getAssert(cls, name):
        module = __import__(name="command_handler.request.validator.asserts", fromlist=[name])
        try:
            return getattr(module, name)
        except AttributeError:
            return cls.asserts[name]

    @classmethod
    def addAssert(cls, name, tester):
        cls.asserts[name] = tester
