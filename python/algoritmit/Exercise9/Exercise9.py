"""

#Task 1
class Solution:

    #Helper function for isBST()
    def is_bst_helper(self, node, min_val, max_val):
        if node is None:
            return True
        if node.data < min_val or node.data > max_val:
            return False
        return self.is_bst_helper(node.left, min_val, node.data - 1) and \
            self.is_bst_helper(node.right, node.data + 1, max_val)
    
    #Function to check whether a Binary Tree is BST or not.
    def isBST(self, root):
        return self.is_bst_helper(root, float('-inf'), float('inf'))
    #Task1 end

    #Task2
    #Helper function of isBalanced()
    def isBalancedHelper(self,node):
        if node is None:
            return 0 #Empty
        return 1 + max(self.isBalancedHelper(node.left), self.isBalancedHelper(node.right))
    
    #Checks absolute difference, 
    def isBalanced(self, root):
        if root is None:
            return True
        
        left_height = self.isBalancedHelper(root.left)
        right_height = self.isBalancedHelper(root.right)

        if abs(left_height - right_height) <= 1:
            return True
        return False
    #Task2 end
        

#{ 
 # Driver Code Starts, from geeksforgeeks.org
from collections import deque
# Tree Node
class Node:
    def __init__(self, val):
        self.right = None
        self.data = val
        self.left = None

# Function to Build Tree   
def buildTree(s):
    #Corner Case
    if(len(s)==0 or s[0]=="N"):           
        return None
        
    # Creating list of strings from input 
    # string after spliting by space
    ip=list(map(str,s.split()))
    
    # Create the root of the tree
    root=Node(int(ip[0]))                     
    size=0
    q=deque()
    
    # Push the root to the queue
    q.append(root)                            
    size=size+1 
    
    # Starting from the second element
    i=1                                       
    while(size>0 and i<len(ip)):
        # Get and remove the front of the queue
        currNode=q[0]
        q.popleft()
        size=size-1
        
        # Get the current node's value from the string
        currVal=ip[i]
        
        # If the left child is not null
        if(currVal!="N"):
            
            # Create the left child for the current node
            currNode.left=Node(int(currVal))
            
            # Push it to the queue
            q.append(currNode.left)
            size=size+1
        # For the right child
        i=i+1
        if(i>=len(ip)):
            break
        currVal=ip[i]
        
        # If the right child is not null
        if(currVal!="N"):
            
            # Create the right child for the current node
            currNode.right=Node(int(currVal))
            
            # Push it to the queue
            q.append(currNode.right)
            size=size+1
        i=i+1
    return root

# } Driver Code Ends
    
test_variable = "2 1 3" #Task 1
test_task2 = "1 2 3 N N 4 6 N 5 N N 7 N" #Task 2

""" #Task 1
"""
if __name__=="__main__":
    t=1
    for _ in range(0,t):
        s = test_variable
        #s=input()
        root=buildTree(s)
        if Solution().isBST(root):
            print(1) 
        else:
            print(0)
""" #Task2
"""
if __name__=="__main__":
    t=1
    for _ in range(0,t):
        s=test_task2
        root=buildTree(s)
        ob = Solution()
        if ob.isBalanced(root):
            print(1) 
        else:
            print(0)
"""

#Task3 in seperate code, it has separate driver code..

#Directly gtg solution
"""
class Solution:

    def insertToAVL(self, root, key): 
        # Step 1 - Perform normal BST 
        if not root: 
            return Node(key) 
        elif key < root.data: 
            root.left = self.insertToAVL(root.left, key) 
        else: 
            root.right = self.insertToAVL(root.right, key) 

        # Step 2 - Update the height of the  
        # ancestor node 
        root.height = 1 + max(self.getHeight(root.left), 
                        self.getHeight(root.right)) 

        # Step 3 - Get the balance factor 
        balance = self.getBalance(root) 

        # Step 4 - If the node is unbalanced,  
        # then try out the 4 cases 
        # Case 1 - Left Left 
        if balance > 1 and key < root.left.data: 
            return self.rightRotate(root) 

        # Case 2 - Right Right 
        if balance < -1 and key > root.right.data: 
            return self.leftRotate(root) 

        # Case 3 - Left Right 
        if balance > 1 and key > root.left.data: 
            root.left = self.leftRotate(root.left) 
            return self.rightRotate(root) 

        # Case 4 - Right Left 
        if balance < -1 and key < root.right.data: 
            root.right = self.rightRotate(root.right) 
            return self.leftRotate(root) 

        return root 
    
    def delete(self, root, key):
 
        # Step 1 - Perform standard BST delete
        if not root:
            return root
 
        elif key < root.val:
            root.left = self.delete(root.left, key)
 
        elif key > root.val:
            root.right = self.delete(root.right, key)
 
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
 
            elif root.right is None:
                temp = root.left
                root = None
                return temp
 
            temp = self.getMinValueNode(root.right)
            root.val = temp.val
            root.right = self.delete(root.right,
                                      temp.val)
 
        # If the tree has only one node,
        # simply return it
        if root is None:
            return root
 
        # Step 2 - Update the height of the 
        # ancestor node
        root.height = 1 + max(self.getHeight(root.left),
                            self.getHeight(root.right))
 
        # Step 3 - Get the balance factor
        balance = self.getBalance(root)
 
        # Step 4 - If the node is unbalanced, 
        # then try out the 4 cases
        # Case 1 - Left Left
        if balance > 1 and self.getBalance(root.left) >= 0:
            return self.rightRotate(root)
 
        # Case 2 - Right Right
        if balance < -1 and self.getBalance(root.right) <= 0:
            return self.leftRotate(root)
 
        # Case 3 - Left Right
        if balance > 1 and self.getBalance(root.left) < 0:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
 
        # Case 4 - Right Left
        if balance < -1 and self.getBalance(root.right) > 0:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)
 
        return root

    def leftRotate(self, z): 

        y = z.right 
        T2 = y.left 

        # Perform rotation 
        y.left = z 
        z.right = T2 

        # Update heights 
        z.height = 1 + max(self.getHeight(z.left), 
                        self.getHeight(z.right)) 
        y.height = 1 + max(self.getHeight(y.left), 
                        self.getHeight(y.right)) 

        # Return the new root 
        return y 

    def rightRotate(self, z): 

        y = z.left 
        T3 = y.right 

        # Perform rotation 
        y.right = z 
        z.left = T3 

        # Update heights 
        z.height = 1 + max(self.getHeight(z.left), 
                        self.getHeight(z.right)) 
        y.height = 1 + max(self.getHeight(y.left), 
                        self.getHeight(y.right)) 

        # Return the new root 
        return y 

    def getHeight(self, root): 
        if not root: 
            return 0

        return root.height 

    def getBalance(self, root): 
        if not root: 
            return 0

        return self.getHeight(root.left) - self.getHeight(root.right) 
    
    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root
 
        return self.getMinValueNode(root.left)

    def preOrder(self, root): 

        if not root: 
            return

        print("{0} ".format(root.val), end="") 
        self.preOrder(root.left) 
        self.preOrder(root.right) 


#{ 
 # Driver Code Starts
#Initial Template for Python 3

class Node:
    def __init__(self,x):
        self.data=x
        self.left=None
        self.right=None
        self.height=1

def isBST(n, lower, upper):
    if not n:
        return True
    
    if n.data <= lower or n.data >= upper:
        return False
    
    return isBST(n.left, lower, n.data) and isBST(n.right, n.data, upper)

def isBalanced(n):
    if not n:
        return (0,True)
    
    lHeight, l = isBalanced(n.left)
    rHeight, r = isBalanced(n.right)
    
    if abs( lHeight - rHeight ) > 1:
        return (0, False)
    
    return ( 1 + max( lHeight,rHeight  ) , l and r )

def isBalancedBST(root):
    if not isBST(root, -1000000000, 1000000000):
        print("BST voilated, inorder traversal :", end=' ')
    
    elif not isBalanced(root)[1]:
        print("Unbalanced BST, inorder traversal :", end=' ')
    
    else:
        return True
    
    return False

def printInorder(n):
    if not n:
        return
    printInorder(n.left)
    print(n.data, end=' ')
    printInorder(n.right)

if __name__=="__main__":
    t = int(input())
    for _ in range(t):
        n = int(input())
        ip = [ int(x) for x in input().strip().split() ]
        
        root = None
        
        for i in range(n):
            root = Solution().insertToAVL( root, ip[i] )
            
            if not isBalancedBST( root ):
                break
        
        printInorder(root)
        print()

# } Driver Code Ends
"""

#Task 3 Delete... for some reason driver code is without using class solution thats present elsewhere.. so I just made it into separate code /
#that removes the class and made every function a generalized function.. Otherwise directly gtg solution.
"""
class Node:
    def __init__(self, x):
        self.data = x
        self.left = None
        self.right = None
        self.height = 1

def insertToAVL(root, key):
    # Step 1 - Perform normal BST 
    if not root: 
        return Node(key) 
    elif key < root.data: 
        root.left = insertToAVL(root.left, key) 
    else: 
        root.right = insertToAVL(root.right, key) 

    # Step 2 - Update the height of the  
    # ancestor node 
    root.height = 1 + max(getHeight(root.left), getHeight(root.right)) 

    # Step 3 - Get the balance factor 
    balance = getBalance(root) 

    # Step 4 - If the node is unbalanced,  
    # then try out the 4 cases 
    # Case 1 - Left Left 
    if balance > 1 and key < root.left.data: 
        return rightRotate(root) 

    # Case 2 - Right Right 
    if balance < -1 and key > root.right.data: 
        return leftRotate(root) 

    # Case 3 - Left Right 
    if balance > 1 and key > root.left.data: 
        root.left = leftRotate(root.left) 
        return rightRotate(root) 

    # Case 4 - Right Left 
    if balance < -1 and key < root.right.data: 
        root.right = rightRotate(root.right) 
        return leftRotate(root) 

    return root 
    
def deleteNode(root, key):
    # Step 1 - Perform standard BST delete
    if not root:
        return root

    elif key < root.data:
        root.left = deleteNode(root.left, key)

    elif key > root.data:
        root.right = deleteNode(root.right, key)

    else:
        if root.left is None:
            temp = root.right
            root = None
            return temp

        elif root.right is None:
            temp = root.left
            root = None
            return temp

        temp = getMinValueNode(root.right)
        root.data = temp.data
        root.right = deleteNode(root.right, temp.data)

    # If the tree has only one node,
    # simply return it
    if root is None:
        return root

    # Step 2 - Update the height of the 
    # ancestor node
    root.height = 1 + max(getHeight(root.left),
                        getHeight(root.right))

    # Step 3 - Get the balance factor
    balance = getBalance(root)

    # Step 4 - If the node is unbalanced, 
    # then try out the 4 cases
    # Case 1 - Left Left
    if balance > 1 and getBalance(root.left) >= 0:
        return rightRotate(root)

    # Case 2 - Right Right
    if balance < -1 and getBalance(root.right) <= 0:
        return leftRotate(root)

    # Case 3 - Left Right
    if balance > 1 and getBalance(root.left) < 0:
        root.left = leftRotate(root.left)
        return rightRotate(root)

    # Case 4 - Right Left
    if balance < -1 and getBalance(root.right) > 0:
        root.right = rightRotate(root.right)
        return leftRotate(root)

    return root

def leftRotate(z):
    y = z.right 
    T2 = y.left 

    # Perform rotation 
    y.left = z 
    z.right = T2 

    # Update heights 
    z.height = 1 + max(getHeight(z.left), getHeight(z.right)) 
    y.height = 1 + max(getHeight(y.left), getHeight(y.right)) 

    # Return the new root 
    return y 

def rightRotate(z):
    y = z.left 
    T3 = y.right 

    # Perform rotation 
    y.right = z 
    z.left = T3 

    # Update heights 
    z.height = 1 + max(getHeight(z.left), getHeight(z.right)) 
    y.height = 1 + max(getHeight(y.left), getHeight(y.right)) 

    # Return the new root 
    return y 

def getHeight(root): 
    if not root: 
        return 0

    return root.height 

def getBalance(root): 
    if not root: 
        return 0

    return getHeight(root.left) - getHeight(root.right) 

def getMinValueNode(root):
    if root is None or root.left is None:
        return root

    return getMinValueNode(root.left)

def preOrder(root): 
    if not root: 
        return

    print("{0} ".format(root.data), end="") 
    preOrder(root.left) 
    preOrder(root.right)

def isBST(n, lower, upper):
    if not n:
        return True
    
    if n.data <= lower or n.data >= upper:
        return False
    
    return isBST(n.left, lower, n.data) and isBST(n.right, n.data, upper)

def isBalanced(n):
    if not n:
        return (0, True)
    
    lHeight, l = isBalanced(n.left)
    rHeight, r = isBalanced(n.right)
    
    if abs(lHeight - rHeight) > 1:
        return (0, False)
    
    return (1 + max(lHeight, rHeight), l and r)

def isBalancedBST(root):
    if not isBST(root, -1000000000, 1000000000):
        print("BST violated, inorder traversal:", end=' ')
    
    elif not isBalanced(root)[1]:
        print("Unbalanced BST, inorder traversal:", end=' ')
    
    else:
        return True
    
    return False

def printInorder(n):
    if not n:
        return
    printInorder(n.left)
    print(n.data, end=' ')
    printInorder(n.right)




#{ 
 # Driver Code Starts
#Initial Template for Python 3

from collections import deque

class Node:
    def __init__(self,x):
        self.data=x
        self.left=None
        self.right=None
        self.height=1

def setHeights(n):
    if not n:
        return 0
    n.height = 1 + max( setHeights(n.left) , setHeights(n.right) )
    return n.height

def buildTree(s):
    #Corner Case
    if(len(s)==0 or s[0]=="N"):           
        return None
        
    # Creating list of strings from input 
    # string after spliting by space
    ip=list(map(str,s.split()))
    
    # Create the root of the tree
    root=Node(int(ip[0]))                     
    size=0
    q=deque()
    
    # Push the root to the queue
    q.append(root)                            
    size=size+1 
    
    # Starting from the second element
    i=1                                       
    while(size>0 and i<len(ip)):
        # Get and remove the front of the queue
        currNode=q[0]
        q.popleft()
        size=size-1
        
        # Get the current node's value from the string
        currVal=ip[i]
        
        # If the left child is not null
        if(currVal!="N"):
            
            # Create the left child for the current node
            currNode.left=Node(int(currVal))
            
            # Push it to the queue
            q.append(currNode.left)
            size=size+1
        # For the right child
        i=i+1
        if(i>=len(ip)):
            break
        currVal=ip[i]
        
        # If the right child is not null
        if(currVal!="N"):
            
            # Create the right child for the current node
            currNode.right=Node(int(currVal))
            
            # Push it to the queue
            q.append(currNode.right)
            size=size+1
        i=i+1
    
    setHeights(root)
    return root

def isBST(n, lower, upper):
    if not n:
        return True
    
    if n.data <= lower or n.data >= upper:
        return False
    
    return isBST(n.left, lower, n.data) and isBST(n.right, n.data, upper)

def isBalanced(n):
    if not n:
        return (0,True)
    
    lHeight, l = isBalanced(n.left)
    rHeight, r = isBalanced(n.right)
    
    if abs( lHeight - rHeight ) > 1:
        return (0, False)
    
    return ( 1 + max( lHeight,rHeight  ) , l and r )

def isBalancedBST(root):
    if not isBST(root, -1000000000, 1000000000):
        print("BST voilated, inorder traversal :", end=' ')
    
    elif not isBalanced(root)[1]:
        print("Unbalanced BST, inorder traversal :", end=' ')
    
    else:
        return True
    
    return False

def printInorder(n):
    if not n:
        return
    printInorder(n.left)
    print(n.data, end=' ')
    printInorder(n.right)

if __name__=="__main__":
    t = int(input())
    for _ in range(t):
        s = input()
        root = buildTree(s)
        
        n = int(input())
        ip = [ int(x) for x in input().split() ]
        
        for i in range(n):
            root = deleteNode( root, ip[i] )
            
            if not isBalancedBST(root):
                break
        
        if root is None:
            print("null")
        else:
            printInorder(root)
            print()

# } Driver Code Ends
"""

#Code from Exercise6, spit the old heapsort into build heap and heapsort separately.
"""
def heapify(arr, n, i):
    largest = i  # Initialize largest as root
    left = 2 * i + 1
    right = 2 * i + 2

    # Check if left child exists and is greater than root
    if left < n and arr[left] > arr[largest]:
        largest = left

    # Check if right child exists and is greater than largest so far
    if right < n and arr[right] > arr[largest]:
        largest = right

    # Change root, if needed
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # Swap
        # Heapify the affected sub-tree
        heapify(arr, n, largest)

def heapsort(arr):
    n = len(arr)

    build_heap(arr)
    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # Swap
        heapify(arr, i, 0)

def build_heap(arr):
    n = len(arr)

    # Build a max heap. n//2 -1 is last non-leaf node, -1 is heap root, step is -1. To change from asc to desc, change step to +1.
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)


#build_heap(arr)
#heapsort(arr)
#print("Heap:", arr)
"""

#gtg variant solution with class Solution

"""
class Solution:
    #Heapify function to maintain heap property.
    def heapify(self,arr, n, i):
        largest = i  # Initialize largest as root
        left = 2 * i + 1
        right = 2 * i + 2
    
        # Check if left child exists and is greater than root
        if left < n and arr[left] > arr[largest]:
            largest = left
    
        # Check if right child exists and is greater than largest so far
        if right < n and arr[right] > arr[largest]:
            largest = right
    
        # Change root, if needed
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]  # Swap
            # Heapify the affected sub-tree
            self.heapify(arr, n, largest)
    
    #Function to build a Heap from array.
    def buildHeap(self,arr, length):
        n = length
        # Build a max heap. n//2 -1 is last non-leaf node, -1 is heap root, step is -1. To change from asc to desc, change step to +1.
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(arr, n, i)
            
    #Function to sort an array using Heap Sort.    
    def HeapSort(self, arr, length):
        n = length
        self.buildHeap(arr, n)
        # Extract elements one by one
        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]  # Swap
            self.heapify(arr, i, 0)

arr = [4, 10, 3, 5, 1]
print(f"Unsorted array: {arr}")
n = len(arr)  
sol = Solution()
sol.HeapSort(arr, n)
print(*arr)
"""
