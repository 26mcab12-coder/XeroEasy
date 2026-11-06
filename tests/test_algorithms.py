import os
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

import app as app_module
import notifications
from dsa.bst import BinaryTree
from dsa.linked_list import OrderLinkedList
from dsa.queue_stack import ActionStack, OrderQueue, evaluate_postfix
from dsa.searching_sorting import insertion_sort, merge_sort, quick_sort

app = app_module.app


DEMOS = (
    "linked-list",
    "queue-stack",
    "postfix-stack",
    "binary-tree",
    "bst",
    "graph-bfs",
    "graph-dfs",
    "linear-search",
    "binary-search",
    "insertion-sort",
    "merge-sort",
    "quick-sort",
    "copy-sort",
    "sorting-comparison",
    "greedy",
    "dynamic-programming",
    "backtracking",
)


class AlgorithmDemoTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_pages_and_assets_load(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertEqual(self.client.get("/algorithms").status_code, 200)
        for asset in ("/static/js/algorithms.js", "/static/css/algorithms.css"):
            response = self.client.get(asset)
            try:
                self.assertEqual(response.status_code, 200)
            finally:
                response.close()

    def test_every_algorithm_demo_runs(self):
        for demo in DEMOS:
            with self.subTest(demo=demo):
                response = self.client.post("/api/algorithms/run", json={"demo": demo})
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.get_json()["success"])

    def test_demo_inputs_are_validated(self):
        self.assertEqual(
            self.client.post("/api/algorithms/run", json={"demo": "unknown"}).status_code,
            400,
        )
        self.assertEqual(
            self.client.post("/api/algorithms/run", json={"demo": "linear-search", "order_id": "30"}).status_code,
            400,
        )
        self.assertEqual(
            self.client.post(
                "/api/algorithms/run",
                json={"demo": "postfix-stack", "expression": "1 0 /"},
            ).status_code,
            400,
        )

    def test_logout_clears_the_session(self):
        with self.client.session_transaction() as session:
            session["account_id"] = 1
            session["role"] = "student"

        self.assertEqual(self.client.post("/api/logout").status_code, 200)
        self.assertEqual(self.client.get("/api/dashboard").status_code, 401)

    def test_dashboard_returns_order_dates_for_weekly_activity(self):
        with self.client.session_transaction() as session:
            session["account_id"] = 1
            session["role"] = "student"

        orders = [{
            "order_id": 42,
            "copies": 3,
            "status": "Completed",
            "order_date": datetime(2026, 10, 22, 12, 30),
            "service_name": "Xerox",
            "price_per_page": 2,
            "student_name": "Alex Student",
        }]
        with (
            patch.object(app_module, "fetch_all", side_effect=[orders, []]),
            patch.object(app_module, "fetch_one", return_value={"name": "Alex Student", "email": "alex@example.com"}),
        ):
            response = self.client.get("/api/dashboard")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["orders"][0]["order_date"], "2026-10-22 12:30:00")

    def test_completing_order_sends_student_email_once(self):
        with self.client.session_transaction() as session:
            session["account_id"] = 1
            session["role"] = "staff"

        previous_order = {"status": "Processing", "name": "Alex Student", "email": "alex@example.com"}
        with (
            patch.object(app_module, "update_order_status", return_value=previous_order),
            patch.object(app_module, "send_order_completed_email", return_value="sent") as send_email,
        ):
            response = self.client.patch("/api/orders/42", json={"status": "Completed"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["email_notification"], "sent")
        send_email.assert_called_once_with("alex@example.com", "Alex Student", 42)

    def test_completed_order_does_not_send_duplicate_email(self):
        with self.client.session_transaction() as session:
            session["account_id"] = 1
            session["role"] = "staff"

        previous_order = {"status": "Completed", "name": "Alex Student", "email": "alex@example.com"}
        with (
            patch.object(app_module, "update_order_status", return_value=previous_order),
            patch.object(app_module, "send_order_completed_email") as send_email,
        ):
            response = self.client.patch("/api/orders/42", json={"status": "Completed"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["email_notification"], "not_needed")
        send_email.assert_not_called()

    def test_email_delivery_failure_is_reported_without_undoing_completion(self):
        with self.client.session_transaction() as session:
            session["account_id"] = 1
            session["role"] = "staff"

        previous_order = {"status": "Processing", "name": "Alex Student", "email": "alex@example.com"}
        with (
            patch.object(app_module, "update_order_status", return_value=previous_order),
            patch.object(
                app_module,
                "send_order_completed_email",
                side_effect=app_module.EmailNotificationError("SMTP unavailable"),
            ),
        ):
            response = self.client.patch("/api/orders/42", json={"status": "Completed"})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["success"])
        self.assertEqual(response.get_json()["email_notification"], "failed")

    def test_completion_email_uses_configured_starttls_smtp(self):
        environment = {
            "XEROEASY_SMTP_HOST": "smtp.example.com",
            "XEROEASY_SMTP_PORT": "587",
            "XEROEASY_SMTP_FROM": "copy@example.com",
            "XEROEASY_SMTP_USERNAME": "copy@example.com",
            "XEROEASY_SMTP_PASSWORD": "test-only-password",
            "XEROEASY_SMTP_USE_TLS": "true",
            "XEROEASY_SMTP_USE_SSL": "false",
        }
        server = MagicMock()
        server.__enter__.return_value = server

        with (
            patch.dict(os.environ, environment, clear=True),
            patch("notifications.smtplib.SMTP", return_value=server) as smtp,
        ):
            result = notifications.send_order_completed_email(
                "student@example.com",
                "Alex Student",
                42,
            )

        self.assertEqual(result, "sent")
        smtp.assert_called_once_with("smtp.example.com", 587, timeout=20)
        server.starttls.assert_called_once()
        server.login.assert_called_once_with("copy@example.com", "test-only-password")
        message = server.send_message.call_args.args[0]
        self.assertEqual(message["To"], "student@example.com")
        self.assertIn("#XE-42", message["Subject"])
        self.assertIn("ready for collection", message.get_content())

    def test_completion_email_reports_missing_smtp_configuration(self):
        with patch.dict(os.environ, {}, clear=True):
            result = notifications.send_order_completed_email(
                "student@example.com",
                "Alex Student",
                42,
            )

        self.assertEqual(result, "not_configured")

    def test_search_and_postfix_results(self):
        response = self.client.post("/api/algorithms/run", json={"demo": "binary-search", "order_id": 20})
        self.assertEqual(response.get_json()["result"]["order"]["order_id"], 20)
        self.assertEqual(evaluate_postfix("5 3 + 2 *"), 16)

    def test_linked_queue_and_stack_edge_cases(self):
        queue = OrderQueue()
        self.assertTrue(queue.is_empty())
        self.assertIsNone(queue.dequeue())
        queue.enqueue("first")
        queue.enqueue("second")
        self.assertEqual(queue.dequeue(), "first")
        self.assertEqual(queue.dequeue(), "second")
        self.assertTrue(queue.is_empty())

        stack = ActionStack()
        self.assertIsNone(stack.pop())
        stack.push("first")
        stack.push("second")
        self.assertEqual(stack.pop(), "second")
        self.assertEqual(stack.pop(), "first")
        self.assertTrue(stack.is_empty())

    def test_sorts_return_sorted_copies(self):
        orders = [{"order_id": value} for value in (4, 1, 3, 2)]
        for sorter in (insertion_sort, merge_sort, quick_sort):
            with self.subTest(sorter=sorter.__name__):
                result = sorter(orders)
                self.assertEqual([order["order_id"] for order in result], [1, 2, 3, 4])
                self.assertEqual([order["order_id"] for order in orders], [4, 1, 3, 2])


    def test_binary_tree_and_linked_list_insert_head(self):
        tree = BinaryTree("Root")
        tree.insert_level_order("Left")
        tree.insert_level_order("Right")
        self.assertEqual(tree.inorder(), ["Left", "Root", "Right"])
        self.assertEqual(tree.preorder(), ["Root", "Left", "Right"])
        self.assertEqual(tree.postorder(), ["Left", "Right", "Root"])

        ll = OrderLinkedList()
        ll.add_order({"order_id": 2})
        ll.insert_head({"order_id": 1})
        self.assertEqual([o["order_id"] for o in ll.display_orders()], [1, 2])

    def test_dashboard_workflow_sorting_and_searching(self):
        with self.client.session_transaction() as session:
            session["account_id"] = 1
            session["role"] = "staff"

        orders = [
            {"order_id": 5, "copies": 12, "status": "Pending", "order_date": datetime(2026, 10, 22, 10, 0), "service_name": "Xerox", "price_per_page": 2, "student_name": "Alice"},
            {"order_id": 2, "copies": 4, "status": "Completed", "order_date": datetime(2026, 10, 22, 11, 0), "service_name": "Printing", "price_per_page": 5, "student_name": "Bob"},
        ]
        with (
            patch.object(app_module, "fetch_all", side_effect=[orders, []]),
            patch.object(app_module, "fetch_one", return_value={"name": "Staff User", "email": "staff@example.com"}),
        ):
            response = self.client.get("/api/dashboard?sort=copies&search_id=2")
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertIn("workflow_dsa", data)
            self.assertEqual(data["workflow_dsa"]["binary_search_result"]["order_id"], 2)


if __name__ == "__main__":
    unittest.main()
