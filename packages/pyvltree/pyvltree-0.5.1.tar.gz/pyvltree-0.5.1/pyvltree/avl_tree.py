from ._avl_node import _AVLNode


class AVLTree():
    """ A recursive implementation of a self-balancing binary search tree.
        Self-balancing is achieved using the AVL algorithms.
    """

    def __init__(self):
        self._root = None

    def search(self, key):
        """ Search for an element given an equivalent key.

            Equivalence is determined based on the elements __eq__ method.

            Time complexity: O(log n)

            Returns the element equivalent to the key if found, None otherwise.
        """

        node = self._root.search(key) if self._root is not None else None

        return node.value if node is not None else None

    def size(self):
        """ Returns the number of elements in the tree.

            Time complexity: O(1)
        """

        return self._root.size if self._root is not None else 0

    def insert(self, value):
        """ Insert an element into the tree.

            Duplicate elements will be silently discarded.

            Time complexity: O(log n)
        """

        self._root = (_AVLNode(value)
                      if self._root is None
                      else self._root.insert(value))

    def delete(self, value):
        """ Deletes an element from the tree.

            Time complexity: O(log n)
        """

        self._root = (self._root.delete(value)
                      if self._root is not None
                      else None)
