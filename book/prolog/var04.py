class Meta(Frame): pass
class Var (Meta ): pass

who = Var('who') ; print who

def person(var):
    var['bound'] = String("Chelsea") ; yield var 
    var['bound'] = String("Hillary") ; yield var
    var['bound'] = String("Bill"   ) ; yield var
for i in person(who): print i