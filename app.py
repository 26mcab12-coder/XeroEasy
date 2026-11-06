from flask import Flask, jsonify, render_template, request, session

# Database functions
from database import (
    fetch_one,
    fetch_all,
    create_student,
    create_order,
    delete_order as delete_order_record,
    restore_order as restore_order_record,
    update_order_status,
)

# MySQL error
from mysql.connector import Error
from notifications import EmailNotificationError, send_order_completed_email

from dsa.advanced_algorithms import (
    greedy_priority_scheduling,
    optimize_printing_jobs,
    schedule_combinations,
)
from dsa.bst import BinaryTree, OrderBST
from dsa.graph import OrderGraph
from dsa.linked_list import OrderLinkedList
from dsa.queue_stack import ActionStack, OrderQueue, evaluate_postfix
from dsa.searching_sorting import (
    binary_search,
    insertion_sort,
    linear_search,
    merge_sort,
    quick_sort,
    sort_by_copies,
)


app = Flask(__name__)

# Flask session secret key
app.secret_key = "xeroeasy-development-key"


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


def _algorithm_sample_orders():
    return [
        {"order_id": 40, "copies": 20, "status": "Pending", "priority": 2},
        {"order_id": 10, "copies": 5, "status": "Completed", "priority": 5},
        {"order_id": 30, "copies": 15, "status": "Processing", "priority": 3},
        {"order_id": 20, "copies": 8, "status": "Pending", "priority": 1},
    ]


@app.get("/algorithms")
def algorithms_page():
    return render_template("algorithms.html")


@app.post("/api/algorithms/run")
def run_algorithm_demo():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(success=False, error="Send a JSON object describing the demo."), 400

    demo = payload.get("demo")
    orders = _algorithm_sample_orders()
    order_id = payload.get("order_id", 30)
    if isinstance(order_id, bool) or not isinstance(order_id, int):
        return jsonify(success=False, error="Order ID must be an integer."), 400

    if demo == "linked-list":
        linked_orders = OrderLinkedList()
        for order in orders:
            linked_orders.add_order(order)
        linked_orders.insert_head({"order_id": 99, "copies": 1, "status": "Pending", "priority": 4})
        count_before_delete = linked_orders.count()
        found_order = linked_orders.find_order(order_id)
        deleted = linked_orders.delete_order(20)
        result = {
            "orders_before_delete": count_before_delete,
            "found_order": found_order,
            "deleted_order_20": deleted,
            "orders_after_delete": linked_orders.display_orders(),
            "remaining_count": linked_orders.count(),
        }
        complexity = "Insert head O(1); Append O(n); find and delete O(n)"
    elif demo == "queue-stack":
        queue = OrderQueue()
        for order in orders:
            queue.enqueue(order)
        next_order = queue.peek()
        processed_order = queue.dequeue()

        actions = ActionStack()
        actions.push({"action": "Created order", "order_id": 10})
        actions.push({"action": "Updated status", "order_id": 10})
        latest_action = actions.peek()
        undone_action = actions.pop()
        result = {
            "queue_next": next_order,
            "queue_processed": processed_order,
            "queue_remaining": queue.display(),
            "stack_latest": latest_action,
            "stack_undo": undone_action,
            "stack_remaining": actions.display(),
        }
        complexity = "Queue enqueue/dequeue O(1); stack push/pop O(1)"
    elif demo == "postfix-stack":
        expression = payload.get("expression", "5 3 + 2 *")
        try:
            value = evaluate_postfix(expression)
        except ValueError as error:
            return jsonify(success=False, error=str(error)), 400
        result = {"expression": expression, "value": value}
        complexity = "O(n) time and O(n) stack space"
    elif demo == "binary-tree":
        tree = BinaryTree("Campus Reprographics Main Desk")
        tree.insert_level_order("Xerox Hub")
        tree.insert_level_order("High-Speed Color Printing")
        tree.insert_level_order("Scanning Center")
        tree.insert_level_order("Express Delivery Desk")
        result = {
            "root": "Campus Reprographics Main Desk",
            "inorder": tree.inorder(),
            "preorder": tree.preorder(),
            "postorder": tree.postorder(),
        }
        complexity = "Level-order insertion O(n); Traversals O(n) time and O(h) space"
    elif demo == "bst":
        tree = OrderBST()
        for order in orders:
            tree.insert(order)
        result = {
            "inorder": tree.inorder(),
            "preorder": tree.preorder(),
            "postorder": tree.postorder(),
            "searched_order": tree.search(order_id),
        }
        complexity = "Search and insertion O(log n) average; O(n) worst case"
    elif demo in {"graph-bfs", "graph-dfs"}:
        graph = OrderGraph()
        graph.add_edge("CSE Department", "Xerox Service")
        graph.add_edge("Xerox Service", "Main Collection Point")
        graph.add_edge("Main Collection Point", "Library")
        graph.add_edge("Library", "Printing Service")
        graph.add_edge("CSE Department", "Printing Service")
        traversal = graph.bfs if demo == "graph-bfs" else graph.dfs
        result = {"graph": graph.display(), "traversal": traversal("CSE Department")}
        complexity = "O(V + E) time and O(V) space"
    elif demo == "linear-search":
        result = {"order_id": order_id, "order": linear_search(orders, order_id)}
        complexity = "O(n) time"
    elif demo == "binary-search":
        result = {
            "order_id": order_id,
            "order": binary_search(insertion_sort(orders), order_id),
            "precondition": "Orders are sorted by order_id.",
        }
        complexity = "O(log n) search after sorting"
    elif demo in {"insertion-sort", "merge-sort", "quick-sort", "copy-sort"}:
        if demo == "insertion-sort":
            sorted_orders = insertion_sort(orders)
            complexity = "O(n^2) time; O(n) extra space"
        elif demo == "merge-sort":
            sorted_orders = merge_sort(orders)
            complexity = "O(n log n) time; O(n) extra space"
        elif demo == "quick-sort":
            sorted_orders = quick_sort(orders)
            complexity = "O(n log n) average; O(n^2) worst case"
        else:
            sorted_orders = sort_by_copies(orders)
            complexity = "O(n^2) time; O(n) extra space"
        result = {"sorted_orders": sorted_orders}
    elif demo == "sorting-comparison":
        result = {
            "insertion_sort": insertion_sort(orders),
            "merge_sort": merge_sort(orders),
            "quick_sort": quick_sort(orders),
            "complexities": {
                "insertion_sort": "O(n^2)",
                "merge_sort": "O(n log n)",
                "quick_sort": "O(n log n) average; O(n^2) worst case",
            },
        }
        complexity = "Compare algorithm growth rates; timings depend on input size and machine."
    elif demo == "greedy":
        result = {"priority_schedule": greedy_priority_scheduling(orders)}
        complexity = "O(n^2) time; O(n) extra space"
    elif demo == "dynamic-programming":
        jobs = [
            {"job_id": "J1", "pages": 10, "value": 60},
            {"job_id": "J2", "pages": 20, "value": 100},
            {"job_id": "J3", "pages": 30, "value": 120},
        ]
        result = {"capacity_pages": 50, **optimize_printing_jobs(jobs, 50)}
        complexity = "O(number of jobs × capacity) time and space"
    elif demo == "backtracking":
        tasks = ["Print Order 1", "Print Order 2", "Print Order 3"]
        schedules = schedule_combinations(tasks, 2)
        result = {"tasks": tasks, "slots": 2, "schedule_count": len(schedules), "schedules": schedules}
        complexity = "O(P(n, k)) time to generate all schedules"
    else:
        return jsonify(success=False, error="Choose a supported algorithm demo."), 400

    return jsonify(success=True, demo=demo, complexity=complexity, result=result)


# =========================================================
# LOGIN
# =========================================================

@app.post("/api/login")
def login():

    payload = request.get_json(silent=True) or {}

    email = payload.get("email", "").strip().lower()
    password = payload.get("password", "")
    role = payload.get("role", "student").strip().lower()

    # Only allow these two roles
    if role not in ("student", "staff"):
        role = "student"

    table = "staff" if role == "staff" else "students"
    id_column = "staff_id" if role == "staff" else "student_id"

    # Validate input
    if not email or not password:
        return jsonify(
            success=False,
            error="Email and password are required."
        ), 400

    try:

        account = fetch_one(
            f"""
            SELECT
                {id_column} AS account_id,
                name,
                email
            FROM {table}
            WHERE LOWER(email) = %s
            AND password = %s
            """,
            (email, password),
        )

    except Error as error:

        print("LOGIN DATABASE ERROR:", error)

        return jsonify(
            success=False,
            error="Database connection unavailable. Check your MySQL settings."
        ), 503

    except Exception as error:

        print("LOGIN ERROR:", error)

        return jsonify(
            success=False,
            error="An unexpected error occurred during login."
        ), 500

    # Account not found
    if not account:
        return jsonify(
            success=False,
            error="Invalid email or password."
        ), 401

    # Store login information in session
    session["account_id"] = account["account_id"]
    session["role"] = role

    return jsonify(
        success=True,
        name=account["name"],
        email=account["email"],
        role=role
    ), 200


# =========================================================
# REGISTER
# =========================================================

@app.post("/api/register")
def register():

    payload = request.get_json(silent=True) or {}

    name = payload.get("name", "").strip()
    email = payload.get("email", "").strip().lower()
    phone = payload.get("phone", "").strip()
    password = payload.get("password", "")

    # Validate input
    if len(name) < 2 or "@" not in email or len(password) < 6:
        return jsonify(
            success=False,
            error="Enter a valid name, college email, and password of at least 6 characters."
        ), 400

    if phone and (not phone.isdigit() or len(phone) < 7):
        return jsonify(
            success=False,
            error="Enter a valid phone number."
        ), 400

    try:

        student_id = create_student(
            name,
            email,
            phone,
            password
        )

    except Error as error:

        print("REGISTER DATABASE ERROR:", error)

        if getattr(error, "errno", None) == 1062:
            return jsonify(
                success=False,
                error="An account with this email already exists."
            ), 409

        return jsonify(
            success=False,
            error="Could not create your account. Check the database connection."
        ), 503

    except Exception as error:

        print("REGISTER ERROR:", error)

        return jsonify(
            success=False,
            error="An unexpected error occurred while creating your account."
        ), 500

    # Automatically log in after registration
    session["account_id"] = student_id
    session["role"] = "student"

    return jsonify(
        success=True,
        name=name,
        email=email,
        role="student"
    ), 201


# =========================================================
# DASHBOARD
# =========================================================

@app.get("/api/dashboard")
def dashboard():

    # Check login
    if "account_id" not in session:
        return jsonify(
            success=False,
            error="Please sign in first."
        ), 401

    role = session["role"]
    account_id = session["account_id"]

    # Students see only their own orders.
    # Staff see all orders.
    order_filter = "" if role == "staff" else "WHERE o.student_id = %s"
    params = () if role == "staff" else (account_id,)

    try:

        orders = fetch_all(
            """
            SELECT
                o.order_id,
                o.copies,
                o.status,
                o.order_date,
                s.service_name,
                s.price_per_page,
                st.name AS student_name
            FROM orders o
            JOIN services s
                ON s.service_id = o.service_id
            JOIN students st
                ON st.student_id = o.student_id
            """
            + order_filter +
            """
            ORDER BY o.order_date DESC
            """,
            params,
        )

        # Get available services
        services = fetch_all(
            """
            SELECT
                service_id,
                service_name,
                price_per_page
            FROM services
            ORDER BY service_name
            """
        )

        # Get student account information
        student = None

        if role == "student":
            student = fetch_one(
                """
                SELECT
                    name,
                    email
                FROM students
                WHERE student_id = %s
                """,
                (account_id,),
            )

    except Error as error:

        print("DASHBOARD DATABASE ERROR:", error)

        return jsonify(
            success=False,
            error="Could not load dashboard data."
        ), 503

    except Exception as error:

        print("DASHBOARD ERROR:", error)

        return jsonify(
            success=False,
            error="An unexpected error occurred while loading the dashboard."
        ), 500

    # Calculate order totals
    for order in orders:

        if order["order_date"]:
            order["order_date"] = order["order_date"].isoformat(
                sep=" "
            )

        order["total"] = (
            float(order["price_per_page"])
            * order["copies"]
        )

    # Count statuses
    status_counts = {
        "Pending": 0,
        "Processing": 0,
        "Completed": 0
    }

    for order in orders:
        status = order["status"]

        status_counts[status] = (
            status_counts.get(status, 0) + 1
        )

    # Workflow Sorting & Searching Integration (Phase 3 & 4)
    sort_param = request.args.get("sort", "").strip().lower()
    search_param = request.args.get("search_id", type=int)
    workflow_dsa = {}

    if sort_param == "copies":
        orders = sort_by_copies(orders)
        workflow_dsa["applied_sort"] = "sort_by_copies (Insertion Sort on copy count)"
    elif sort_param in ("order_id", "merge", "asc"):
        orders = merge_sort(orders, key="order_id")
        workflow_dsa["applied_sort"] = "merge_sort (O(n log n) stable sort by order_id)"
    elif sort_param == "quick":
        orders = quick_sort(orders, key="order_id")
        workflow_dsa["applied_sort"] = "quick_sort (O(n log n) average pivot sort)"
    elif sort_param in ("greedy", "priority"):
        orders = greedy_priority_scheduling(orders)
        workflow_dsa["applied_sort"] = "greedy_priority_scheduling (Urgent priority dispatch)"

    if search_param:
        sorted_for_search = insertion_sort(orders)
        searched = binary_search(sorted_for_search, search_param)
        workflow_dsa["binary_search_result"] = searched
        workflow_dsa["search_technique"] = "Binary Search O(log n) after Insertion Sort"

    # Return dashboard data
    return jsonify(
        success=True,
        role=role,
        account=student,
        orders=orders,
        workflow_dsa=workflow_dsa,
        services=services,

        summary={
            "total_orders": len(orders),

            "active_orders":
                status_counts.get("Pending", 0)
                + status_counts.get("Processing", 0),

            "pending_orders":
                status_counts.get("Pending", 0),

            "processing_orders":
                status_counts.get("Processing", 0),

            "completed_orders":
                status_counts.get("Completed", 0),

            "total_copies":
                sum(
                    order["copies"]
                    for order in orders
                ),

            "total_value":
                round(
                    sum(
                        order["total"]
                        for order in orders
                    ),
                    2
                ),
        },
    )


# =========================================================
# CREATE ORDER
# =========================================================

@app.post("/api/orders")
def add_order():

    # Only students can create orders
    if session.get("role") != "student":
        return jsonify(
            success=False,
            error="Only students can create orders."
        ), 403

    payload = request.get_json(silent=True) or {}

    try:

        service_id = int(payload["service_id"])
        copies = int(payload["copies"])

        if copies < 1:
            raise ValueError

        # Check service exists
        service = fetch_one(
            """
            SELECT service_id
            FROM services
            WHERE service_id = %s
            """,
            (service_id,),
        )

        if not service:
            raise ValueError

        # Create order
        order_id = create_order(
            session["account_id"],
            service_id,
            copies
        )

    except (KeyError, ValueError):

        return jsonify(
            success=False,
            error="Choose a service and enter at least one copy."
        ), 400

    except Error as error:

        print("ORDER DATABASE ERROR:", error)

        return jsonify(
            success=False,
            error="Could not create the order."
        ), 503

    return jsonify(
        success=True,
        order_id=order_id,
        status="Pending"
    ), 201


# =========================================================
# DELETE ORDER
# =========================================================

@app.delete("/api/orders/<int:order_id>")
def delete_order(order_id):

    if session.get("role") != "student" or "account_id" not in session:
        return jsonify(
            success=False,
            error="Only students can delete their own orders."
        ), 403

    try:
        deleted = delete_order_record(order_id, session["account_id"])
        if not deleted:
            return jsonify(
                success=False,
                error="Order not found."
            ), 404

    except Error as error:
        app.logger.error("DELETE ORDER DATABASE ERROR: %s", error)
        return jsonify(
            success=False,
            error="Could not delete the order."
        ), 503

    return jsonify(
        success=True,
        order_id=order_id,
    ), 200


@app.post("/api/orders/<int:order_id>/restore")
def restore_order(order_id):

    if session.get("role") != "student" or "account_id" not in session:
        return jsonify(
            success=False,
            error="Only students can restore their own orders."
        ), 403

    try:
        restored = restore_order_record(order_id, session["account_id"])
        if not restored:
            return jsonify(
                success=False,
                error="Deleted order not found."
            ), 404

    except Error as error:
        app.logger.error("RESTORE ORDER DATABASE ERROR: %s", error)
        return jsonify(
            success=False,
            error="Could not restore the order."
        ), 503

    return jsonify(
        success=True,
        order_id=order_id,
    ), 200


# =========================================================
# UPDATE ORDER STATUS
# =========================================================

@app.patch("/api/orders/<int:order_id>")
def update_order(order_id):

    # Only staff can update orders
    if session.get("role") != "staff":
        return jsonify(
            success=False,
            error="Only staff can update order status."
        ), 403

    payload = request.get_json(silent=True) or {}
    status = payload.get("status", "")

    # Check valid status
    if status not in {
        "Pending",
        "Processing",
        "Completed"
    }:
        return jsonify(
            success=False,
            error="Status must be Pending, Processing, or Completed."
        ), 400

    try:

        previous_order = update_order_status(order_id, status)
        if previous_order is None:
            return jsonify(
                success=False,
                error="Order not found."
            ), 404

    except Error as error:

        print("UPDATE ORDER DATABASE ERROR:", error)

        return jsonify(
            success=False,
            error="Could not update order status."
        ), 503

    email_notification = "not_needed"
    if status == "Completed" and previous_order["status"] != "Completed":
        try:
            email_notification = send_order_completed_email(
                previous_order["email"],
                previous_order["name"],
                order_id,
            )
        except EmailNotificationError as error:
            app.logger.warning("Completion email failed for order %s: %s", order_id, error)
            email_notification = "failed"

    return jsonify(
        success=True,
        order_id=order_id,
        status=status,
        email_notification=email_notification,
    ), 200


# =========================================================
# LOGOUT
# =========================================================

@app.post("/api/logout")
def logout():

    session.clear()

    return jsonify(
        success=True,
        message="Logged out successfully."
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )