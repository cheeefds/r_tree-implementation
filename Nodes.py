class Entry:
    def __init__(self, mbr, child=None, data=None):
        self.mbr = mbr  #[xmin,xmax,ymin,ymax]
        self.child = child
        self.data = data
        
    def is_leaf_entry(self):
        return self.data is not None

class Node:
    def __init__(self, is_leaf=True, parent = None):
        self.is_leaf = is_leaf
        self.children = []
        self.parent = parent
        self.children_count = 0
        
    
    