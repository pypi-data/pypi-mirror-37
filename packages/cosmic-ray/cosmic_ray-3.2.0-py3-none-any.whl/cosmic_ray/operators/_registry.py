_REGISTERED_OPERATORS = set()


def register_operator(cls):
    _REGISTERED_OPERATORS.add(cls)
    return cls
