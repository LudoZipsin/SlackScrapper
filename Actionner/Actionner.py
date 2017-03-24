import inspect


class Actionner:
    def __init__(self):
        self.list_exclude_methods = ["__init__", "__str__", "__repr__", "get_relevant_methods"]
        pass

    def get_relevant_methods(self) -> list:
        return [meth[0] for meth in inspect.getmembers(self, predicate=inspect.ismethod) if meth[0] not in self.list_exclude_methods]
