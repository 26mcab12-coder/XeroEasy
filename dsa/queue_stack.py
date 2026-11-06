import math


class _Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class OrderQueue:
    """
    Queue for processing orders using FIFO.

    FIFO = First In First Out
    """

    def __init__(self):
        self._front = None
        self._back = None
        self._size = 0

    def enqueue(self, order):
        """
        Add order to the queue.
        """
        node = _Node(order)

        if self._back is None:
            self._front = node
        else:
            self._back.next = node

        self._back = node
        self._size += 1

    def dequeue(self):
        """
        Remove the oldest order.
        """
        if self._front is None:
            return None

        order = self._front.value
        self._front = self._front.next
        self._size -= 1

        if self._front is None:
            self._back = None

        return order

    def peek(self):
        """
        View the next order without removing it.
        """
        return None if self._front is None else self._front.value

    def is_empty(self):
        return self._size == 0

    def size(self):
        return self._size

    def display(self):
        result = []
        current = self._front

        while current is not None:
            result.append(current.value)
            current = current.next

        return result


class ActionStack:
    """
    Stack for storing recent actions.

    LIFO = Last In First Out
    """

    def __init__(self):
        self._top = None
        self._size = 0

    def push(self, action):
        """
        Add an action.
        """
        node = _Node(action)
        node.next = self._top
        self._top = node
        self._size += 1

    def pop(self):
        """
        Remove the most recent action.
        """
        if self._top is None:
            return None

        action = self._top.value
        self._top = self._top.next
        self._size -= 1
        return action

    def peek(self):
        """
        View the latest action.
        """
        return None if self._top is None else self._top.value

    def is_empty(self):
        return self._size == 0

    def size(self):
        return self._size

    def display(self):
        result = []
        current = self._top

        while current is not None:
            result.append(current.value)
            current = current.next

        return result


def evaluate_postfix(expression):
    """Evaluate a whitespace-separated postfix arithmetic expression."""
    if not isinstance(expression, str) or not expression.strip():
        raise ValueError("Enter a postfix expression.")

    tokens = expression.split()
    if len(tokens) > 200:
        raise ValueError("The expression cannot contain more than 200 tokens.")

    operators = {
        "+": lambda left, right: left + right,
        "-": lambda left, right: left - right,
        "*": lambda left, right: left * right,
        "/": lambda left, right: left / right,
    }
    values = ActionStack()

    for token in tokens:
        if token in operators:
            right = values.pop()
            left = values.pop()
            if left is None or right is None:
                raise ValueError("The expression does not have enough operands.")
            if token == "/" and right == 0:
                raise ValueError("Division by zero is not allowed.")
            values.push(operators[token](left, right))
            continue

        try:
            number = float(token)
        except ValueError as error:
            raise ValueError(f"Invalid number or operator: {token}") from error

        if not math.isfinite(number):
            raise ValueError("Numbers must be finite.")
        values.push(int(number) if number.is_integer() else number)

    result = values.pop()
    if result is None or not values.is_empty():
        raise ValueError("The expression must resolve to exactly one value.")
    return result


if __name__ == "__main__":

    print("===== QUEUE =====")

    order_queue = OrderQueue()

    order_queue.enqueue({
        "order_id": 1,
        "copies": 5
    })

    order_queue.enqueue({
        "order_id": 2,
        "copies": 10
    })

    order_queue.enqueue({
        "order_id": 3,
        "copies": 15
    })

    print("Queue:")
    print(order_queue.display())

    print("\nNext Order:")
    print(order_queue.peek())

    print("\nProcessing Order:")
    print(order_queue.dequeue())

    print("\nQueue After Processing:")
    print(order_queue.display())

    print("\n===== STACK =====")

    action_stack = ActionStack()

    action_stack.push({
        "action": "Created Order",
        "order_id": 1
    })

    action_stack.push({
        "action": "Updated Status",
        "order_id": 1
    })

    action_stack.push({
        "action": "Completed Order",
        "order_id": 1
    })

    print("Actions:")
    print(action_stack.display())

    print("\nLatest Action:")
    print(action_stack.peek())

    print("\nUndo Action:")
    print(action_stack.pop())

    print("\nActions After Undo:")
    print(action_stack.display()) 