class Lattice(object):

    def __init__(self,length,width,height):
        self.length = length
        self.wideth = width
        self.height = height

    def __eq__(self,other):
        if self is other:
            return True
        if type(self) != type(other):
            return False
        elif self.length == other.length and self.width == other.width and \
             self.height == other.height:
            return True
        else:
            return False

    def latticeProtect(self):
        if self.width < 0 or self.length < 0 or self.height < 0:
            raise ValueError("Inappropriate entries lattice cannot \
                             exist")
    def nodeNumber(self):
        """Returns the total number of nodes in the Cayley tree. """
        if self.height < 0:
            return self.length*self.width
        return self.height*self.width*self.length

    def linkCreator(self):
        link_d = dict()
        for n in list(range(self.nodeNumber())):
            if n%self.length != 0:
                link_d[n] = [n+1]
##            if True:
##                link_d[n]
            
            
