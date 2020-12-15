def slurp(path: str) -> str:
    with open(path) as fd:
        return fd.read()

# def or_else(val: Optional[T], default: T) -> T:
#     if val is None:
#         return default
#     else:
#         return val