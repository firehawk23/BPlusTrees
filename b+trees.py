import pickle
class Node():
    def __init__(self,order=4):
        self.order = order
        self.keys = []
        self.values = []
        self.leaf = True

    def isempty(self):  #Checks  whether keys empty or not
      return len(self.keys)==0
    
    def isfull(self):    #Checks if keys are full or not
        return len(self.keys) == self.order
    
    def add(self, key, value):
        if not self.keys: # If the node is empty, insert the new key-value pair
            self.keys.append(key)
            self.values.append([value])
            return None

        for i, item in enumerate(self.keys):
            if key == item: #If new key matches with the existing key, add it to the list of values
                if not value in self.values[i]:
                    self.values[i].append(value)
                    break

            # If new key is smaller than the existing key, insert new key to the left of the existing key
            elif key < item:
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                self.values = self.values[:i] + [[value]] + self.values[i:]
                break

            elif i + 1 == len(self.keys): #If newkey is larger than all existing keys,insert newkey to the right of all existing keys
                self.keys.append(key)
                self.values.append([value])

    def split(self):
        left = Node(self.order)
        right = Node(self.order)
        mid = self.order//2
        left.keys = self.keys[:mid]
        left.values = self.values[:mid]
        right.keys = self.keys[mid:]
        right.values = self.values[mid:]
        self.keys = [right.keys[0]]
        self.values = [left, right]
        self.leaf = False

    def display(self,l=0):
        print("Level ", l, ":   ", str(self.keys))
        if not self.leaf:
            for i in self.values:
                i.display(l+1)

class BPlusTree():
    def __init__(self,order=4):
        self.order = order
        self.root = Node(self.order)

    def insert(self,value,key):
        parent = None
        child = self.root
        while not child.leaf: #Traverse until leaf node is reached.
            parent = child
            child, index = self.find(child,key)
        child.add(key, value)
        if child.isfull(): # If leaf node is full,then split leaf node into two.
            child.split()
            if parent and not parent.isfull(): # after split a internal node and two leaf nodes needs to be re-inserted back into the tree.
                self.merge(parent, child, index)
    
    def find(self, node, key):# Returns list of value in index and index where we need to insert the key

        for i, item in enumerate(node.keys):
            if key < item:
                return node.values[i], i
        return node.values[i+1], i+1

    def merge(self, parent, child, index):
        parent.values.pop(index)
        pivot = child.keys[0]
        for i, item in enumerate(parent.keys):
            if pivot < item:
                parent.keys = parent.keys[:i] + [pivot] + parent.keys[i:]
                parent.values = parent.values[:i] + child.values + parent.values[i:]
                break

            elif i + 1 == len(parent.keys):
                parent.keys += [pivot]
                parent.values += child.values
                break

    def lookup(self, key): #Returns value for given key
        if(len(key)<25):
            key= key.ljust(25," ")
        else:
            key= key[:25]
        curr_node = self.root
        while not curr_node.leaf:
              curr_node,index = self.find(curr_node, key)
        for i, item in enumerate(curr_node.keys):
            if key == item:
                return curr_node.values[i]
        return -1

    def search(self, key):  #Returns location of value for given key
        current_node = self.root
        while(current_node.leaf == False):
            temp = current_node.keys
            for i in range(len(temp)):
                if (key == temp[i]):
                    current_node = current_node.values[i + 1]
                    break
                elif (key < temp[i]):
                    current_node = current_node.values[i]
                    break
                elif (i + 1 == len(current_node.keys)):
                    current_node = current_node.values[i + 1]
                    break
        return current_node

    def delete(self,key):
        if(len(key) < 25):
            key = key.ljust(25," ")
        else:
            key = key[:25]
        value = self.lookup(key)[0]
        curr_node = self.search(key)
        temp = 0
        for i, item in enumerate(curr_node.keys):
            if item == key:
                temp = 1
                if value in curr_node.values[i]:
                    if len(curr_node.values[i]) > 1:
                        curr_node.values[i].pop(curr_node.values[i].index(value))
                    elif curr_node == self.root:
                        curr_node.keys.pop(i)
                        curr_node.values.pop(i)
                    else:
                        curr_node.values[i].pop(curr_node.values[i].index(value))
                        del curr_node.values[i]
                        curr_node.keys.pop(curr_node.keys.index(key))
                    print("Deleted")
                else:
                    print("Value not in Key")
                    return
        if temp == 0:
            print("Value not in Tree")
            return

    def display(self):
        self.root.display()

bt = BPlusTree(4)
with open("a.txt", "r") as f1:
    for i,line in enumerate(f1):
        line2 = line.strip()
        if(len(line2)<25):
            k= line2.ljust(25," ")
        else:
            k= line2[:25]
        bt.insert(i+1,k)

with open("/content/drive/MyDrive/MTCS-203(P)-Assignment/index.txt", 'wb') as fp: # writing contents of Bplustree in Binary
    pickle.dump(bt,fp)

with open("/content/drive/MyDrive/MTCS-203(P)-Assignment/index.txt", 'rb') as fp1: # reading contents of Bplustree in Binary
    tree = pickle.load(fp1)
    tree.display()