def FIND():
    T = S.pop()
    try: S // W[T.value] ; return True
    except KeyError: S // T ; return False
W << FIND
