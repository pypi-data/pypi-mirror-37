class IfCondition(object):
    NAME = 'if'

    def __init__(self, configuration, factory):
        self.path = factory.get_path(configuration["path"])

    def evaluate(self, namespace, extracted):
        obj = self.path.read_from(namespace).obj

        return isinstance(obj, bool) and obj
