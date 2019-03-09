class String(Primitive):
    def str(self):
        S = ''
        for c in self.value:
            if    c == '\n': S += '\\n'
            elif  c == '\t': S += '\\t'
            else: S += c
        return S
