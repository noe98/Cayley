class Lattice(object):

    def __init__(self,length,width,height):
        self.x = length
        self.y = width
        self.z = height

    def __eq__(self,other):
        if self is other:
            return True
        if type(self) != type(other):
            return False
        elif self.x == other.x and self.y == other.y and \
             self.z == other.z:
            return True
        else:
            return False

    def latticeProtect(self):
        if self.y < 0 or self.x < 0 or self.z < 0:
            raise ValueError("Inappropriate entries lattice cannot \
                             exist")
    def nodeNumber(self):
        """Returns the total number of nodes in the Lattice."""
        if self.z < 0:
            return self.x*self.y
        return self.z*self.y*self.x

    def linkCreator(self):
        link_d = dict()
        #in x-direction
        for count in range(self.x*self.y):
            if count % self.x == 0:
                link_d[count] = [count+1]
            elif count % self.x == self.x-1:
                link_d[count] = [count-1]
            elif count-1<0:
                link_d[count] = [count+1]
            else:
                link_d[count+1] = [count-1]
                link_d[count] = link_d.get(count+1,list()) + [count+1]
                
        #in y-direction
        for count in range(self.x*self.y):
            if count >= (self.x*self.y)-self.x:
                link_d[count] = link_d.get(count,list())+ [count-self.x]
                link_d[count-self.x] = link_d.get(count-self.x,list()) + [count]
            else:
                if count+self.x >= (self.x*self.y)-self.x:
                    pass
                else:
                    link_d[count+self.x] = link_d.get(count+self.x,list()) + [count]
                    link_d[count] = link_d.get(count,list()) + [count+self.x]
        #in-z-dirction
        
        return link_d
    
