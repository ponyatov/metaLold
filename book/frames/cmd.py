class CMD(Active):
    def __init__(self,F):
        Active.__init__(self,F.__name__)
        self.fn = F
    def execute(self):
        self.fn()