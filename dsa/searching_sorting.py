def linear_search(orders, order_id):
    """
    Linear Search.

    Checks each order one by one.
    """

    for order in orders:

        if order["order_id"] == order_id:
            return order

    return None


def binary_search(orders, order_id):
    """
    Binary Search.

    Orders must be sorted by order_id.
    """

    low = 0
    high = len(orders) - 1

    while low <= high:

        middle = (low + high) // 2

        current_id = orders[middle]["order_id"]

        if current_id == order_id:
            return orders[middle]

        elif order_id < current_id:
            high = middle - 1

        else:
            low = middle + 1

    return None


def insertion_sort(orders):
    """
    Insertion Sort.

    Sort orders according to order ID.
    """

    result = orders.copy()

    for i in range(1, len(result)):

        current = result[i]
        j = i - 1

        while j >= 0 and result[j]["order_id"] > current["order_id"]:

            result[j + 1] = result[j]
            j -= 1

        result[j + 1] = current

    return result


def merge_sort(orders, key="order_id"):
    """Return a stable merge-sorted copy of orders."""
    if len(orders) < 2:
        return orders.copy()

    middle = len(orders) // 2
    left = merge_sort(orders[:middle], key)
    right = merge_sort(orders[middle:], key)
    result = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index][key] <= right[right_index][key]:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1

    result.extend(left[left_index:])
    result.extend(right[right_index:])
    return result


def quick_sort(orders, key="order_id"):
    """Return a quick-sorted copy of orders without changing the input."""
    result = orders.copy()

    def partition(low, high):
        pivot = result[high][key]
        boundary = low

        for index in range(low, high):
            if result[index][key] <= pivot:
                result[boundary], result[index] = result[index], result[boundary]
                boundary += 1

        result[boundary], result[high] = result[high], result[boundary]
        return boundary

    def sort(low, high):
        if low < high:
            pivot_index = partition(low, high)
            sort(low, pivot_index - 1)
            sort(pivot_index + 1, high)

    sort(0, len(result) - 1)
    return result


def sort_by_copies(orders):
    """
    Insertion sort based on number of copies.
    """

    result = orders.copy()

    for i in range(1, len(result)):

        current = result[i]
        j = i - 1

        while j >= 0 and result[j]["copies"] > current["copies"]:

            result[j + 1] = result[j]
            j -= 1

        result[j + 1] = current

    return result


if __name__ == "__main__":

    orders = [
        {
            "order_id": 40,
            "copies": 20,
            "status": "Pending"
        },
        {
            "order_id": 10,
            "copies": 5,
            "status": "Completed"
        },
        {
            "order_id": 30,
            "copies": 15,
            "status": "Processing"
        },
        {
            "order_id": 20,
            "copies": 8,
            "status": "Pending"
        }
    ]

    print("===== SEARCHING AND SORTING =====")

    print("\nOriginal Orders:")
    print(orders)

    print("\nLinear Search - Order 30:")
    print(linear_search(orders, 30))

    sorted_orders = insertion_sort(orders)

    print("\nSorted Orders:")
    print(sorted_orders)

    print("\nBinary Search - Order 20:")
    print(binary_search(sorted_orders, 20))

    print("\nSorted By Copies:")
    print(sort_by_copies(orders))