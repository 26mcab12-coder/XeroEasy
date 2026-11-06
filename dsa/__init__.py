"""
DSA Package for XeroEasy Reprographics Management System.
Implements linear structures, trees, graphs, sorting/searching, and advanced algorithms.
"""

from .linked_list import OrderNode, OrderLinkedList
from .queue_stack import OrderQueue, ActionStack, evaluate_postfix
from .bst import BinaryTreeNode, BinaryTree, BSTNode, OrderBST
from .graph import OrderGraph
from .searching_sorting import (
    linear_search,
    binary_search,
    insertion_sort,
    merge_sort,
    quick_sort,
    sort_by_copies,
)
from .advanced_algorithms import (
    greedy_priority_scheduling,
    optimize_printing_jobs,
    schedule_combinations,
)

__all__ = [
    "OrderNode",
    "OrderLinkedList",
    "OrderQueue",
    "ActionStack",
    "evaluate_postfix",
    "BinaryTreeNode",
    "BinaryTree",
    "BSTNode",
    "OrderBST",
    "OrderGraph",
    "linear_search",
    "binary_search",
    "insertion_sort",
    "merge_sort",
    "quick_sort",
    "sort_by_copies",
    "greedy_priority_scheduling",
    "optimize_printing_jobs",
    "schedule_combinations",
]

