class Dict(Container):
    
  # operator dict[slot]=obj
  def __setitem__(self,slot,obj):
    # if function?
    if callable(obj):
      self[slot] = VM(obj) ; return self
    else: return Container.__setitem__(self, slot, obj)
    
  # operator dict << obj
  def __lshift__(self,obj):
    # if function?
    if callable(obj):
      self << VM(obj) ; return self
    else: return Container.__lshift__(self, obj)