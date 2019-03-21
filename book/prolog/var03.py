def person(var):
    var = "Chelsea" ; yield var 
    var = "Hillary" ; yield var
    var = "Bill"    ; yield var
who = None  # create variable
for i in person(who): print i

Chelsea
Hillary
Bill