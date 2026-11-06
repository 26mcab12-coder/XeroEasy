class BinaryTreeNode:
    """
    Node for a general structured Binary Tree.
    """

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinaryTree:
    """
    Binary Tree for structured hierarchical data storage
    (e.g., campus service hierarchy, document categories).
    Implements the complete tree traversal set: Inorder, Preorder, Postorder.
    """

    def __init__(self, root_data=None):
        self.root = BinaryTreeNode(root_data) if root_data is not None else None

    def insert_level_order(self, data):
        """
        Insert structured data in level-order into the binary tree.
        """
        new_node = BinaryTreeNode(data)
        if self.root is None:
            self.root = new_node
            return

        queue = [self.root]
        while queue:
            current = queue.pop(0)
            if current.left is None:
                current.left = new_node
                return
            queue.append(current.left)

            if current.right is None:
                current.right = new_node
                return
            queue.append(current.right)

    def inorder(self):
        """
        Inorder Traversal: Left -> Root -> Right
        """
        result = []

        def traverse(node):
            if node is not None:
                traverse(node.left)
                result.append(node.data)
                traverse(node.right)

        traverse(self.root)
        return result

    def preorder(self):
        """
        Preorder Traversal: Root -> Left -> Right
        """
        result = []

        def traverse(node):
            if node is not None:
                result.append(node.data)
                traverse(node.left)
                traverse(node.right)

        traverse(self.root)
        return result

    def postorder(self):
        """
        Postorder Traversal: Left -> Right -> Root
        """
        result = []

        def traverse(node):
            if node is not None:
                traverse(node.left)
                traverse(node.right)
                result.append(node.data)

        traverse(self.root)
        return result


class BSTNode:
    """
    Node for Binary Search Tree.
    """

    def __init__(self, order):
        self.order = order
        self.left = None
        self.right = None


class OrderBST:
    """
    Binary Search Tree for organizing orders by order ID for efficient O(log n) data access.
    """

    def __init__(self):
        self.root = None

    def insert(self, order):
        """
        Insert an order into the BST.
        """

        if self.root is None:
            self.root = BSTNode(order)
            return

        self._insert(self.root, order)

    def _insert(self, node, order):

        order_id = order["order_id"]

        if order_id < node.order["order_id"]:

            if node.left is None:
                node.left = BSTNode(order)
            else:
                self._insert(node.left, order)

        elif order_id > node.order["order_id"]:

            if node.right is None:
                node.right = BSTNode(order)
            else:
                self._insert(node.right, order)

    def search(self, order_id):
        """
        Search order by ID in O(log n) average time.
        """

        current = self.root

        while current is not None:

            if order_id == current.order["order_id"]:
                return current.order

            if order_id < current.order["order_id"]:
                current = current.left
            else:
                current = current.right

        return None

    def inorder(self):
        """
        Left -> Root -> Right
        """

        result = []

        def traverse(node):

            if node is not None:
                traverse(node.left)
                result.append(node.order)
                traverse(node.right)

        traverse(self.root)

        return result

    def preorder(self):
        """
        Root -> Left -> Right
        """

        result = []

        def traverse(node):

            if node is not None:
                result.append(node.order)
                traverse(node.left)
                traverse(node.right)

        traverse(self.root)

        return result

    def postorder(self):
        """
        Left -> Right -> Root
        """

        result = []

        def traverse(node):

            if node is not None:
                traverse(node.left)
                traverse(node.right)
                result.append(node.order)

        traverse(self.root)

        return result


if __name__ == "__main__":

    print("===== BINARY TREE (STRUCTURED STORAGE) =====")
    bt = BinaryTree("XeroEasy Reprographics")
    bt.insert_level_order("Xerox Hub")
    bt.insert_level_order("Printing Lab")
    bt.insert_level_order("Scanning Desk")
    print("Inorder:", bt.inorder())
    print("Preorder:", bt.preorder())
    print("Postorder:", bt.postorder())

    print("\n===== BINARY SEARCH TREE (EFFICIENT ACCESS) =====")
    bst = OrderBST()
    bst.insert({"order_id": 50, "copies": 10, "status": "Pending"})
    bst.insert({"order_id": 30, "copies": 5, "status": "Processing"})
    bst.insert({"order_id": 70, "copies": 20, "status": "Completed"})
    bst.insert({"order_id": 20, "copies": 3, "status": "Pending"})
    bst.insert({"order_id": 40, "copies": 8, "status": "Completed"})

    print("Inorder:", bst.inorder())
    print("Preorder:", bst.preorder())
    print("Postorder:", bst.postorder())
    print("Search Order 40:", bst.search(40))
