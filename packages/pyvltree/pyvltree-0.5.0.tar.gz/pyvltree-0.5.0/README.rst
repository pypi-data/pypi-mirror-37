===========
PYVLTree
===========

Simple implementation of an AVL Tree.

Usage::

    #!/usr/bin/env python

    from pyvltree import AVLTree
    
    tree = AVLTree()
    tree.insert(3)
    three = tree.search(3)
    n = tree.size()
    tree.delete(3)
