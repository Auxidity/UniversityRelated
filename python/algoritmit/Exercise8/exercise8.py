from graphviz import Digraph
from IPython.display import SVG
from collections import deque


'''
graphviz and ipython.display are used to visualize the generated tree.

This code defines a Node data structure with attributes value, left and right. Value is the integer value stored in node. 
Attribute left is a pointer to the left child of a node, once initialized it's None.
Attribute right is a pointer to the right child, correspondingly.

The Binary Search Tree (BST) data structure is a tree consisting of nodes. The left sub-tree consists of all values less than 
the value of the node, the right sub-tree of all values greater than the current node value.

The BST data structure has functions:
* add a node
* delete a node
* search a node
* preorder traversal (DF traversal)
* inorder traversal (DF traversal)
* postorder traversal (DF traversal)
* print for all traverlsal types
* visualise for graphical print
'''

class Node:
    def __init__(self,value):
        self.value = value
        self.left = None
        self.right = None
        
class BST:
    def __init__(self):
        self.root = None
        
    def _add(self, current, value):
        
        if self.root == None:
            self.root = Node(value)
        else:
            if value < current.value:
                if current.left == None:
                    current.left = Node(value)
                else:
                    self._add(current.left, value)
            else:
                if current.right == None:
                    current.right = Node(value)
                else:
                    self._add(current.right, value)
      
    def add(self, value):
        new_node = Node(value)
        
        if self.root == None:
            self.root = new_node
            
        else:
             self._add(self.root, value)
    
    def delete(self,root, key):
        """
        Delete a node with the given key from a binary search tree.

        :param root: The root of the binary search tree.
        :param key: The value of the node to be deleted.
        :return: The new root of the binary search tree.
        """
        if not root:
            return None

        if key < root.value:
            root.left = self.delete(root.left, key)
        elif key > root.value:
            root.right = self.delete(root.right, key)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            else:
                temp = self.find_min(root.right)
                root.value = temp.value
                root.right = self.delete(root.right, temp.value)

        return root

    def find_min(self,root):
        while root.left:
            root = root.left
        return root
        
    # returns a node whose value == input value
    # if no node with input value is found, None is returned
    def _search(self, node, value):
        if node is None or node.value == value:
            return node          
        
        if value < node.value:
            return self._search(node.left, value)
        else:
            return self._search(node.right,value) 
        
    # prints the result of search: does a node with input value exist in the BST or not                   
    def search(self, value):
        result = self._search(self.root,value)
        
        if result is None:
            print(f"NO node with value {value} found in BST!")
        elif result.value == value:
            print(f"YES, a node with value {value} found in BST!")
    
    
    # visiting = print the value of the node
    def visit(self, node):
        print(node.value)
    
    # There are different types of in-depth traversals: pre-order, in-order and post-order
    # Here's an algorithm for all those
    
    # pre-order traversal
    def preorder(self, current):
        if current is not None:
            self.visit(current)
            self.preorder(current.left)
            self.preorder(current.right)
        
    def preprint(self):
        self.preorder(self.root)

    # inorder traversal
    def inorder(self, current):
        if current is not None:
            self.inorder(current.left)
            self.visit(current)
            self.inorder(current.right)
    
    def inprint(self):
        self.inorder(self.root)

    #postorder traversal
    def postorder(self, current):
        if current is not None:
            self.postorder(current.left)
            self.postorder(current.right)
            self.visit(current)
            
    def postprint(self):
        self.postorder(self.root)
    
    def level_order_traversal(self,root):
        """
        Perform level-order traversal on a binary tree.

        :param root: The root of the binary tree.
        :return: A list containing the values in the binary tree in level-order traversal order.
        """
        if not root:
            return []

        res = []
        q = deque([root])

        while q:
            level_size = len(q)
            level_vals = []
            for _ in range(level_size):
                node = q.popleft()
                level_vals.append(node.value)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            res.append(level_vals)

        return res

    def levelprint(self):
        levellist = self.level_order_traversal(self.root)
        for item in levellist:
            print(item)
                
    # visualize the BST with graphviz digraph
    def visualize(self):
        dot = Digraph(comment='Binary Tree')
        
        def add_nodes_edges(node):
            if node is None:
                return
            dot.node(str(node.value), str(node.value))
            if node.left is not None:
                dot.edge(str(node.value), str(node.left.value))
                add_nodes_edges(node.left)
            if node.right is not None:
                dot.edge(str(node.value), str(node.right.value))
                add_nodes_edges(node.right)
        
        add_nodes_edges(self.root)
        return SVG(dot.pipe(format='svg'))
    
    #Task2
    def find_max(self, node):
        current= node
        while current.right is not None:
            current = current.right

        return current.value
    
    def find_maximum(self):
        if self.root is None:
            return None
        return self.find_max(self.root)
    
    def find_mini(self, node):
        current= node
        while current.left is not None:
            current = current.left

        return current.value
    
    def find_minimum(self):
        if self.root is None:
            return None
        return self.find_mini(self.root)
    
    #Task3
    def find_height(self, node):
        if node is None:
            return -1
        else:
            left_height = self.find_height(node.left)
            right_height = self.find_height(node.right)
            return 1 + max(left_height, right_height)
    
    def find_depth(self, root, node, depth=0):
        if root is None or node is None:
            return -1
        if root.value ==  node.value:
            return depth
        left_depth = self.find_depth(root.left, node, depth+1)
        right_depth = self.find_depth(root.right, node, depth+1)

        if left_depth != -1:
            return left_depth
        else:
            return right_depth
    
    #Task5
    #Helper function for list approach
    def _inorder_traversal(self, current, result):
        if current is not None:
            if current.left is not None:
                self._inorder_traversal(current.left, result)
            result.append(current.value)
            if current.right is not None:
                self._inorder_traversal(current.right, result)
    
    #Another helper function for list approach
    def _inorder_traversal_list(self):
        if self.root is None:
            return []
        result = []
        self._inorder_traversal(self.root, result)
        return result
    
    def inorder_list(self, value, pred_or_succ):
        list = self._inorder_traversal_list()

        if pred_or_succ == "pred":
            for i in range(len(list)):
                if list[i] == value:
                    if i > 0:
                        return list[i - 1]
                    else:
                        return "No predecessor"
            print(f"no node with {value}")

        elif pred_or_succ == "succ":
            for i in range(len(list)):
                if list[i] == value:
                    if i < len(list) - 1:
                        return list[i + 1]
                    else:
                        return "No successor"
            print(f"No node with {value}")

        else:
            print("Invalid argument on pred || succ")

    # Bst approach
    def inorder_predecessor(self, node, value):
        predecessor = None
        while node is not None:
            if node.value == value:
                if node.left is not None:
                    predecessor = node.left
                    while predecessor.right is not None:
                        predecessor = predecessor.right
                break
            elif node.value < value:
                predecessor = node
                node = node.right
            else:
                node = node.left
        
        if predecessor is not None:
            return predecessor.value
        else:
            return "No predecessor"
    
    def inorder_successor(self, node, value):
        succ = None
        while node is not None:
            if node.value == value:
                if node.right is not None:
                    succ = node.right
                    while succ.left is not None:
                        succ = succ.left
                break
            elif node.value < value:
                node = node.right
            else:
                succ = node
                node = node.left
        
        if succ is not None:
            return succ.value
        else:
            return "No successor"


# Driver code here!

#Task1
bst = BST()

elements = [7,10,3,6,12,15,2,5,11]

for element in elements:
    bst.add(element)

SVG_tree = bst.visualize() #Can't view this in terminal

with open('bst_tree.svg', 'w') as file: 
    file.write(SVG_tree.data) #Open this file in VSCode with a svg previewer


#Task 2
"""
bst.search(6)
bst.search(5)
bst.search(13)
bst.search(4)

bst_largest = bst.find_maximum()

print(bst_largest)
print(bst.find_minimum())
"""

#Task 3
"""
root_height = bst.find_height(bst.root)
root_depth = bst.find_depth(bst.root, bst.root)

leaf_value = 11
leaf_node = bst._search(bst.root, leaf_value)

if leaf_node is not None:
    leaf_depth = bst.find_depth(bst.root, leaf_node)
    leaf_height = bst.find_height(leaf_node)
    print(f"{leaf_depth} depth, {leaf_height} height on leaf node {leaf_value}")
else:
    print (f"{leaf_value} not found in BST")

internal_value = 6
internal_node = bst._search(bst.root, internal_value)

if internal_node is not None:
    internal_depth = bst.find_depth(bst.root, internal_node)
    internal_height = bst.find_height(internal_node)
    print(f"{internal_depth} depth, {internal_height} height on internal node {internal_value}")
else:
    print (f"{internal_value} not found in BST")
"""

#Task 4_leaf
"""
bst_1 = BST()

elements = [7,10,3,6,12,15,2,5,11]

for element in elements:
    bst_1.add(element)

bst_1.delete(bst_1.root, 2)

SVG_tree_leaf = bst_1.visualize() #Can't view this in terminal

with open('bst_tree_leaf.svg', 'w') as file: 
    file.write(SVG_tree_leaf.data) #Open this file in VSCode with a svg previewer

#Task 4_1child

bst_2 = BST()

elements = [7,10,3,6,12,15,2,5,11]

for element in elements:
    bst_2.add(element)

bst_2.delete(bst_2.root,6)

SVG_tree_1child = bst_2.visualize() #Can't view this in terminal

with open('bst_tree_1child.svg', 'w') as file: 
    file.write(SVG_tree_1child.data) #Open this file in VSCode with a svg previewer

#Task 4_2child

bst_3 = BST()

elements = [7,10,3,6,12,15,2,5,11]

for element in elements:
    bst_3.add(element)

bst_3.delete(bst_3.root,12)

SVG_tree_2child = bst_3.visualize() #Can't view this in terminal

with open('bst_tree_2child.svg', 'w') as file: 
    file.write(SVG_tree_2child.data) #Open this file in VSCode with a svg previewer

"""

#Task5
key = 15


print(bst.inorder_predecessor(bst.root, key))
print(bst.inorder_successor(bst.root, key))

print(bst.inorder_list(key,"succ"))