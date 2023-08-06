class _AVLNode():
    _BALANCE_FACTOR_LIMIT = 2;

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.size = 1
        self._height = 0
        self._balance_factor = 0

    def search(self, key):
        if key == self.value:
            return self
        elif key < self.value:
            return self.left.search(key) if self._has_left_child() else None
        else:
            return self.right.search(key) if self._has_right_child() else None

    def insert(self, value):
        if value == self.value:
            new_height = self._height
        elif value < self.value:
            if self.left is None:
                self.left = _AVLNode(value)
                new_height = max(self._height, 1)
            else:
                self.left = self.left.insert(value)
                new_height = (max(self._height, self.left._height + 1)
                              if self._has_left_child()
                              else self._height)
        else:
            if self.right is None:
                self.right = _AVLNode(value)
                new_height = max(self._height, 1)
            else:
                self.right = self.right.insert(value)
                new_height = (max(self._height, self.right._height + 1)
                              if self._has_right_child()
                              else self._height)

        self._height = new_height
        self._balance_factor = self._calculate_balance_factor()

        if self._needs_rebalancing():
            new_subtree_root = self._rebalance()
        else:
            new_subtree_root = self

        self.size = self._recalculate_size()

        return new_subtree_root

    def delete(self, value):
        new_subtree_root = self

        if value < self.value:
            self.left = (self.left.delete(value)
                         if self.left is not None
                         else None)
        elif value > self.value:
            self.right = (self.right.delete(value)
                          if self.right is not None
                          else None)
        elif self._has_two_children():
            self.value = self.right._min().value
            self.right = self.right.delete(self.value)
        else:
            new_subtree_root = (self.left
                                if self.left is not None
                                else self.right)

        self._height = self._recalculate_height()
        self._balance_factor = self._calculate_balance_factor()

        if self._needs_rebalancing():
            new_subtree_root = self._rebalance()

        self.size = self._recalculate_size()

        return new_subtree_root

    def _min(self):
        return self.left._min() if self._has_left_child() else self

    def _needs_rebalancing(self):
        return abs(self._balance_factor) >= _AVLNode._BALANCE_FACTOR_LIMIT

    def _calculate_balance_factor(self):
        right_subtree_height = (self.right._height
                                if self._has_right_child()
                                else -1)
        left_subtree_height = (self.left._height
                               if self._has_left_child()
                               else -1)

        return right_subtree_height - left_subtree_height

    def _rebalance(self):
        if self.right is None:
            tallest_child = self.left
        elif self.left is None:
            tallest_child = self.right
        else:
            tallest_child = (self.right
                             if self.right._height > self.left._height
                             else self.left)

        if tallest_child is self.left:
            if tallest_child._is_right_heavy():     # Left-Right
                return (self._rotate_right(
                        tallest_child._rotate_left(tallest_child.right)))
            else:                                   # Left-Left
                return self._rotate_right(tallest_child)
        elif tallest_child is self.right:
            if tallest_child._is_left_heavy():      # Right-Left
                return (self._rotate_left(
                        tallest_child._rotate_right(tallest_child.left)))
            else:                                   # Right-Right
                return self._rotate_left(tallest_child)

    def _rotate_left(self, pivot):
        self.right = pivot.left
        pivot.left = self

        self._height = self._recalculate_height()
        pivot._height = pivot._recalculate_height()
        self._balance_factor = self._calculate_balance_factor()
        pivot.balance_factor = pivot._calculate_balance_factor()
        self.size = self._recalculate_size()
        pivot.size = pivot._recalculate_size()

        return pivot

    def _rotate_right(self, pivot):
        self.left = pivot.right
        pivot.right = self

        self._height = self._recalculate_height()
        pivot._height = pivot._recalculate_height()
        self._balance_factor = self._calculate_balance_factor()
        pivot.balance_factor = pivot._calculate_balance_factor()
        self.size = self._recalculate_size()
        pivot.size = pivot._recalculate_size()

        return pivot

    def _recalculate_height(self):
        return max(self.left._height if self._has_left_child() else -1,
                   self.right._height if self._has_right_child() else -1) + 1

    def _recalculate_size(self):
        size = 1

        if self._has_left_child():
            size += self.left.size
        if self._has_right_child():
            size += self.right.size

        return size

    def _has_two_children(self):
        return self._has_left_child() and self._has_right_child()

    def _has_left_child(self):
        return self.left is not None

    def _has_right_child(self):
        return self.right is not None

    def _is_right_heavy(self):
        return self._balance_factor > 0

    def _is_left_heavy(self):
        return self._balance_factor < 0
