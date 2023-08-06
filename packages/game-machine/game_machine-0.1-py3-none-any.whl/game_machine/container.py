class Container (object) :
    """
    A Container allows a hierarchy of visual objects to be constructed

    A container is either a single object, in which case a call to its
    draw method calls the draw method of the child class, or if it is
    not single, then it maintains a list of child instances, and a call to
    draw calls the draw method on all the child instances.
    """
    def __init__(self) :
        super(Container, self).__init__()
        self.children = []

    def add(self, child) :
        self.children.append(child)

    def remove(self, child) :
        index = -1
        for i, c in enumerate(self.children) :
            if c == child :
                index = i
        if index != -1 :
            del self.children[index]
    
