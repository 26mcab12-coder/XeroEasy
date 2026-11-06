class OrderNode:
    """
    A single node in the order linked list.
    """

    def __init__(self, order):
        self.order = order
        self.next = None


class OrderLinkedList:
    """
    Linked List used to manage XeroEasy orders.
    """

    def __init__(self):
        self.head = None

    def insert_head(self, order):
        """
        Insert a new order at the head of the list in O(1) time.
        """
        new_node = OrderNode(order)
        new_node.next = self.head
        self.head = new_node

    def add_order(self, order):
        """
        Add a new order to the end of the list.
        """

        new_node = OrderNode(order)

        # If list is empty
        if self.head is None:
            self.head = new_node
            return

        # Find the last node
        current = self.head

        while current.next is not None:
            current = current.next

        current.next = new_node

    def delete_order(self, order_id):
        """
        Delete an order using its order ID.
        """

        if self.head is None:
            return False

        # Delete first node
        if self.head.order["order_id"] == order_id:
            self.head = self.head.next
            return True

        current = self.head

        while current.next is not None:

            if current.next.order["order_id"] == order_id:
                current.next = current.next.next
                return True

            current = current.next

        return False

    def find_order(self, order_id):
        """
        Find an order using its order ID.
        """

        current = self.head

        while current is not None:

            if current.order["order_id"] == order_id:
                return current.order

            current = current.next

        return None

    def display_orders(self):
        """
        Return all orders stored in the linked list.
        """

        orders = []

        current = self.head

        while current is not None:
            orders.append(current.order)
            current = current.next

        return orders

    def count(self):
        """
        Return number of orders in the linked list.
        """

        count = 0
        current = self.head

        while current is not None:
            count += 1
            current = current.next

        return count
