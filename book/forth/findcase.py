# ( token -- object|token )
def FIND():
    T = S.pop()
    try: S // W[T.str()]             ; return True
    except KeyError:
        try: S // W[T.str().upper()] ; return True
        except KeyError: S // T      ; return False
W << FIND