import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self,other):
        return other.x == self.x and other.y ==self.y
        
class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
    def contains(self, point):
        return (point.x >= self.x - self.w) and \
            (point.x < self.x + self.w) and \
            (point.y >= self.y - self.h) and \
            (point.y < self.y + self.h);
    
    def intersects(self, rect):
        return not (rect.x - rect.w > self.x + self.w or \
          rect.x + rect.w < self.x - self.w or \
          rect.y - rect.h > self.y + self.h or \
          rect.y + rect.h < self.y - self.h);
        
class QuadTree:
    def __init__(self, boundary, n):
        self.capacity = n
        self.boundary = boundary
        self.points = []
        self.divided = False
    
    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h
        ne = Rectangle(x + w / 2, y - h / 2, w / 2, h / 2)
        self.northeast = QuadTree(ne, self.capacity)
        nw = Rectangle(x - w / 2, y - h / 2, w / 2, h / 2)
        self.northwest = QuadTree(nw, self.capacity)
        se = Rectangle(x + w / 2, y + h / 2, w / 2, h / 2)
        self.southeast = QuadTree(se, self.capacity)
        sw = Rectangle(x - w / 2, y + h / 2, w / 2, h / 2)
        self.southwest = QuadTree(sw, self.capacity)
        self.divided = True
        
        
    def insert(self,point):
        if(not self.boundary.contains(point)):
            return False
        
        if len(self.points) < self.capacity :
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()
                
            if self.northeast.insert(point):
                return True
            elif self.northwest.insert(point):
                return True
            elif self.southeast.insert(point):
                return True
            elif self.southwest.insert(point):
                return True
            
    def join_helper(self,tmp, found):
        if tmp is not None:
            for t in tmp:
                if t not in found:
                    found.append(t)
        return found
    
    def query(self, query, found = []):
        if not found:
            found = []
        
        if not self.boundary.intersects(query):
            return []
        else:
            for p in self.points:
                if query.contains(p):
                    found.append(p)
            if (self.divided):
                tmp = self.northwest.query(query,found)
                self.join_helper(tmp, found)
                tmp = self.northeast.query(query,found)
                self.join_helper(tmp, found)
                tmp = self.southwest.query(query,found)
                self.join_helper(tmp, found)
                tmp = self.southeast.query(query,found)
                self.join_helper(tmp, found)
                
        return found
    
    def show(self, ax = None):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h
        if ax is None:
            fig1 = plt.figure()
            ax = fig1.add_subplot(111, aspect='equal')

        ax.add_patch(patches.Rectangle((x, y), 2*w, 2*h,fill=False))
        
        for p in self.points:
            ax.scatter(p.x,p.y, color = "k")
        
        if self.divided:
          self.northwest.show(ax)
          self.northeast.show(ax)
          self.southeast.show(ax)
          self.southwest.show(ax)
        
        return ax
        
        
