import unittest
from unittest.mock import MagicMock, patch

import app as app_module
import database


class OrderDeletionTests(unittest.TestCase):
    def setUp(self):
        app_module.app.config["TESTING"] = True
        self.client = app_module.app.test_client()

    def test_student_can_delete_owned_order(self):
        with self.client.session_transaction() as session:
            session["account_id"] = 7
            session["role"] = "student"

        with patch.object(app_module, "delete_order_record", return_value=True) as delete_order:
            response = self.client.delete("/api/orders/42")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"success": True, "order_id": 42})
        delete_order.assert_called_once_with(42, 7)

    def test_student_cannot_delete_order_they_do_not_own(self):
        with self.client.session_transaction() as session:
            session["account_id"] = 7
            session["role"] = "student"

        with patch.object(app_module, "delete_order_record", return_value=False):
            response = self.client.delete("/api/orders/42")

        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.get_json()["success"])

    def test_staff_cannot_delete_orders(self):
        with self.client.session_transaction() as session:
            session["account_id"] = 3
            session["role"] = "staff"

        with patch.object(app_module, "delete_order_record") as delete_order:
            response = self.client.delete("/api/orders/42")

        self.assertEqual(response.status_code, 403)
        delete_order.assert_not_called()

    def test_deleting_order_requires_student_session(self):
        with self.client.session_transaction() as session:
            session["role"] = "student"

        response = self.client.delete("/api/orders/42")

        self.assertEqual(response.status_code, 403)

    def test_database_failure_is_reported(self):
        with self.client.session_transaction() as session:
            session["account_id"] = 7
            session["role"] = "student"

        with patch.object(
            app_module,
            "delete_order_record",
            side_effect=app_module.Error("database unavailable"),
        ):
            response = self.client.delete("/api/orders/42")

        self.assertEqual(response.status_code, 503)
        self.assertFalse(response.get_json()["success"])

    def test_student_can_restore_owned_order(self):
        with self.client.session_transaction() as session:
            session["account_id"] = 7
            session["role"] = "student"

        with patch.object(app_module, "restore_order_record", return_value=True) as restore_order:
            response = self.client.post("/api/orders/42/restore")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"success": True, "order_id": 42})
        restore_order.assert_called_once_with(42, 7)

    def test_student_cannot_restore_order_they_do_not_own(self):
        with self.client.session_transaction() as session:
            session["account_id"] = 7
            session["role"] = "student"

        with patch.object(app_module, "restore_order_record", return_value=False):
            response = self.client.post("/api/orders/42/restore")

        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.get_json()["success"])

    def test_staff_cannot_restore_orders(self):
        with self.client.session_transaction() as session:
            session["account_id"] = 3
            session["role"] = "staff"

        with patch.object(app_module, "restore_order_record") as restore_order:
            response = self.client.post("/api/orders/42/restore")

        self.assertEqual(response.status_code, 403)
        restore_order.assert_not_called()

    def test_database_delete_is_scoped_to_student_and_committed(self):
        connection = MagicMock()
        connection.cursor.return_value.fetchone.return_value = {
            "order_id": 42,
            "student_id": 7,
            "service_id": 2,
            "copies": 5,
            "status": "Pending",
            "order_date": None,
        }

        with patch.object(database, "get_connection", return_value=connection):
            deleted = database.delete_order(42, 7)

        self.assertTrue(deleted)
        execute_calls = connection.cursor.return_value.execute.call_args_list
        self.assertEqual(len(execute_calls), 3)
        self.assertIn("WHERE order_id = %s AND student_id = %s", execute_calls[0].args[0])
        self.assertIn("INSERT INTO deleted_orders", execute_calls[1].args[0])
        self.assertEqual(execute_calls[1].args[1], (42, 7, 2, 5, "Pending", None))
        self.assertEqual(
            execute_calls[2],
            unittest.mock.call(
            "DELETE FROM orders WHERE order_id = %s AND student_id = %s",
            (42, 7),
            ),
        )
        connection.commit.assert_called_once()
        connection.rollback.assert_not_called()
        connection.close.assert_called_once()

    def test_database_restore_preserves_order_and_commits(self):
        connection = MagicMock()
        connection.cursor.return_value.fetchone.return_value = {
            "order_id": 42,
            "student_id": 7,
            "service_id": 2,
            "copies": 5,
            "status": "Pending",
            "order_date": None,
        }

        with patch.object(database, "get_connection", return_value=connection):
            restored = database.restore_order(42, 7)

        self.assertTrue(restored)
        execute_calls = connection.cursor.return_value.execute.call_args_list
        self.assertEqual(len(execute_calls), 3)
        self.assertIn("WHERE order_id = %s AND student_id = %s", execute_calls[0].args[0])
        self.assertIn("INSERT INTO orders", execute_calls[1].args[0])
        self.assertEqual(execute_calls[1].args[1], (42, 7, 2, 5, "Pending", None))
        self.assertIn("DELETE FROM deleted_orders", execute_calls[2].args[0])
        connection.commit.assert_called_once()
        connection.rollback.assert_not_called()
        connection.close.assert_called_once()

    def test_database_delete_rolls_back_if_order_is_missing(self):
        connection = MagicMock()
        connection.cursor.return_value.fetchone.return_value = None

        with patch.object(database, "get_connection", return_value=connection):
            deleted = database.delete_order(42, 7)

        self.assertFalse(deleted)
        connection.cursor.return_value.execute.assert_called_once()
        connection.rollback.assert_called_once()
        connection.commit.assert_not_called()
        connection.close.assert_called_once()
        connection.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
