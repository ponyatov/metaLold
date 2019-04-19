# расширенная фреймовая модель [Marvin Minsky]
class Frame:
    # конструктор фрейма с заданным именем
    def __init__(self,V):
        # метка класса/типа (для упрощения использована строка)
        self.type  = self.__class__.__name__.lower()
        # атомарное значение фрейма (примитивный тип Python)
        # хранит имя фрейма, или строку, число,..
        self.value = V
        # slots/attributes /associative array/
        self.attr  = {}
        # nested objects /ordered list = stack/
        self.nest  = []
 
print Frame('hello')
<frame:hello>