# bst.py
# ===================================================
# Implement a binary search tree that can store any
# arbitrary object in the tree.
# ===================================================


class Student:
    def __init__(self, number, name):
        self.grade = number  # this will serve as the object's key
        self.name = name

    def __lt__(self, kq):
        return self.grade < kq.grade

    def __gt__(self, kq):
        return self.grade > kq.grade

    def __eq__(self, kq):
        return self.grade == kq.grade

    def __str__(self):
        if self.grade is not None:
            return f"Grade: {self.grade}, Name: {self.name}"

class TreeNode:
    def __init__(self, val):
        self.left = None
        self.right = None
        self.val = val  # when this is a primitive, this serves as the node's key

    def __repr__(self):
        return f"TreeNode Containing: {self.val}"


class BST:
    def __init__(self, start_tree=None) -> None:
        """ Initialize empty tree """
        self.root = None

        # populate tree with initial nodes (if provided)
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self):
        """
        Traverses the tree using "in-order" traversal
        and returns content of tree nodes as a text string
        """
        values = [str(_) for _ in self.in_order_traversal()]
        return "TREE in order { " + ", ".join(values) + " }"

    def add(self, val):
        """
        Creates and adds a new node to the BSTree.
        If the BSTree is empty, the new node should added as the root.

        Args:
            val: Item to be stored in the new node
        """
        parent_node = None
        current_node = self.root
        new_node = TreeNode(val)

        while current_node is not None: # Checks if current node is none
            parent_node = current_node # Moves parent node to current node
            if new_node.val < current_node.val:
                current_node = current_node.left # Moves current node down the left side of tree
            else:
                current_node = current_node.right # Moves current node down the right side of tree

        if self.root == None:
            self.root = new_node # If root is none, re-assign root.
        else:
            current_node = new_node  # Assign current node as new leaf.

            if current_node.val < parent_node.val: # Re-assigns parents left/right pointers.
                parent_node.left = current_node
            else:
                parent_node.right = current_node

    def in_order_traversal(self, cur_node=None, visited=None) -> []:
            """
            Perform in-order traversal of the tree and return a list of visited nodes
            """
            if visited is None:
                # first call to the function -> create container to store list of visited nodes
                # and initiate recursive calls starting with the root node
                visited = []
                self.in_order_traversal(self.root, visited)

            # not a first call to the function
            # base case - reached the end of current subtree -> backtrack
            if cur_node is None:
                return visited

            # recursive case -> sequence of steps for in-order traversal:
            # visit left subtree, store current node value, visit right subtree
            self.in_order_traversal(cur_node.left, visited)
            visited.append(cur_node.val)
            self.in_order_traversal(cur_node.right, visited)
            return visited

    def pre_order_traversal(self, cur_node=None, visited=None) -> []:
        """
        Perform pre-order traversal of the tree and return a list of visited nodes

        Returns:
            A list of nodes in the specified ordering
        """
        if visited is None:
            # first call to the function -> create container to store list of visited nodes
            # and initiate recursive calls starting with the root node
            visited = []
            self.pre_order_traversal(self.root, visited)

            # not a first call to the function
            # base case - reached the end of current subtree -> backtrack
        if cur_node is None:
            return visited

        # recursive case -> sequence of steps for in-order traversal:
        # visit left subtree, store current node value, visit right subtree
        visited.append(cur_node.val) # Record node on first visit.
        self.pre_order_traversal(cur_node.left, visited)
        self.pre_order_traversal(cur_node.right, visited)
        return visited

    def post_order_traversal(self, cur_node=None, visited=None) -> []:
        """
        Perform post-order traversal of the tree and return a list of visited nodes

        Returns:
            A list of nodes in the specified ordering
        """
        if visited is None:
            # first call to the function -> create container to store list of visited nodes
            # and initiate recursive calls starting with the root node
            visited = []
            self.post_order_traversal(self.root, visited)

            # not a first call to the function
            # base case - reached the end of current subtree -> backtrack
        if cur_node is None:
            return visited

        # recursive case -> sequence of steps for in-order traversal:
        # visit left subtree, store current node value, visit right subtree
        self.post_order_traversal(cur_node.left, visited)
        self.post_order_traversal(cur_node.right, visited)
        visited.append(cur_node.val)  # Record node on third visit.
        return visited

    def contains(self, kq):
        """
        Searches BSTree to determine if the query key (kq) is in the BSTree.

        Args:
            kq: query key

        Returns:
            True if kq is in the tree, otherwise False
        """
        current_node = self.root
        while current_node is not None: # Keep searching if current node is not none
            if current_node.val == kq: # Return True when kq is found
                return True
            elif kq < current_node.val: # Move to left node if kq < current_node
                current_node = current_node.left
            else:
                current_node = current_node.right # Move to right node if kq >= current_node

        return False # Return false if kq is not found

    def left_child(self, node):
        """
        Returns the left-most child in a subtree.

        Args:
            node: the root node of the subtree

        Returns:
            The left-most node of the given subtree
        """
        current_node = node
        while current_node is not None: # Ensure that tree is not empty.
            while current_node.left is not None: # Ensure left node is not empty.
                current_node = current_node.left # Re-assign current_node
            return current_node # Return value of current_node

    def remove(self, kq):

        """
        Removes node with key k, if the node exists in the BSTree.

        Args:
            node: root of Binary Search Tree
            kq: key of node to remove

        Returns:
            True if k is in the tree and successfully removed, otherwise False
        """
        child_flag = None # Keeps track of which child we are in from direct parent.
        parent_node = None
        successor_parent = None
        successor_node = None
        current_node = self.root

        while current_node is not None: # Keep searching if current_node is not none.
            if current_node.val == kq: # If found delete value, adjust tree, return true
                if current_node.left is not None and current_node.right is not None: # If the node has two children, find in order successor, and replace the node, fix connections.
                    successor_node = current_node.right # Enter right subtree

                    if successor_node.left is None: # If the successor is the first node of the subtree, only update its left side
                        successor_node.left = current_node.left  # Records current nodes left side (as successors new left)
                    else: # Find the farthest left node in the right subtree, and update successor.left, successor_parent.left, and successor.right
                        while successor_node.left is not None:
                            successor_parent = successor_node
                            successor_node = successor_node.left

                        successor_node.left = current_node.left # Record current nodes left side (as successors new left)
                        successor_parent.left = successor_node.right # Record successor nodes right side (as successors parents left side)
                        successor_node.right = current_node.right # Record current nodes right side (as successors right side)

                    if parent_node is None:
                        self.root = successor_node
                    else:
                        if child_flag == "left": # Record parents new link, left or right.
                            parent_node.left = successor_node
                        else:
                            parent_node.right = successor_node

                elif current_node.left is not None or current_node.right is not None: # If node being deleted only has 1 child, have parent point to it's child instead.
                    if current_node.left is not None: # Check if the child is in the left node
                        if parent_node is None:
                            self.root = current_node.left
                        else:
                            if child_flag == "left": # Check if the node is on the parents left side
                                parent_node.left = current_node.left
                            else: # The node is on the parents right side
                                parent_node.right = current_node.left

                    else: # The child is in the right node
                        if parent_node is None:
                            self.root = current_node.right
                        else:
                            if child_flag == "left": # Check if the node is on the parents left side
                                parent_node.left = current_node.right
                            else: # The node is on the parents right side
                                parent_node.right = current_node.right

                else: # If node being deleted has no children, remove it from parent.
                    if parent_node is None:
                        self.root = None
                    else:
                        if child_flag == "left":
                            parent_node.left = None
                        else:
                            parent_node.right = None

                return True
            elif kq < current_node.val: # Move to left node if kq < current_node
                parent_node = current_node
                child_flag = "left"
                current_node = current_node.left
            else: # Move to right node if kq >= current_node
                parent_node = current_node
                child_flag = "right"
                current_node = current_node.right
        return False

    def get_first(self):
        """
        Gets the val of the root node in the BSTree.

        Returns:
            val of the root node, return None if BSTree is empty
        """
        if self.root is not None:
            return self.root.val
        else:
            return self.root

    def remove_first(self):
        """
        Removes the val of the root node in the BSTree.

        Returns:
            True if the root was removed, otherwise False
        """
        if self.root is not None: # If root is not None call remove with root.val as the argument
            self.remove(self.root.val)
            return True
        else:
            return False