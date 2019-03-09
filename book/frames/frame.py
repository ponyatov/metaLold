# extended frame model [Marvin Minsky]
class Frame:
    # construct frame with given name
    def __init__(self,V):
        # class/type tag (string for simplicity)
        self.type  = self.__class__.__name__.lower()
        # atomic value (Python primitive type)
        self.value = V
        # slots/attributes /associative array/
        self.attr  = {}
        # nested objects /ordered list = stack/
        self.nest  = []
 
print Frame('hello')
<frame:hello>