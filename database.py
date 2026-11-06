import os

import mysql.connector
from mysql.connector import Error


def get_connection():
	return mysql.connector.connect(
		host=os.getenv("XEROEASY_DB_HOST", "127.0.0.1"),
		port=int(os.getenv("XEROEASY_DB_PORT", "3306")),
		user=os.getenv("XEROEASY_DB_USER", "root"),
		password=os.getenv("XEROEASY_DB_PASSWORD", "MySQL@123"),
		database=os.getenv("XEROEASY_DB_NAME", "xeroeasy"),
	)


def fetch_one(query, params=()):
	connection = get_connection()
	try:
		cursor = connection.cursor(dictionary=True)
		cursor.execute(query, params)
		return cursor.fetchone()
	finally:
		connection.close()


def fetch_all(query, params=()):
	connection = get_connection()
	try:
		cursor = connection.cursor(dictionary=True)
		cursor.execute(query, params)
		return cursor.fetchall()
	finally:
		connection.close()


def create_order(student_id, service_id, copies):
	connection = get_connection()
	try:
		cursor = connection.cursor()
		cursor.execute(
			"INSERT INTO orders (student_id, service_id, copies) VALUES (%s, %s, %s)",
			(student_id, service_id, copies),
		)
		connection.commit()
		return cursor.lastrowid
	finally:
		connection.close()


def delete_order(order_id, student_id):
	connection = get_connection()
	try:
		cursor = connection.cursor(dictionary=True)
		cursor.execute(
			"""
			SELECT order_id, student_id, service_id, copies, status, order_date
			FROM orders
			WHERE order_id = %s AND student_id = %s
			FOR UPDATE
			""",
			(order_id, student_id),
		)
		order = cursor.fetchone()
		if order is None:
			connection.rollback()
			return False

		cursor.execute(
			"""
			INSERT INTO deleted_orders
				(order_id, student_id, service_id, copies, status, order_date)
			VALUES (%s, %s, %s, %s, %s, %s)
			""",
			(
				order["order_id"],
				order["student_id"],
				order["service_id"],
				order["copies"],
				order["status"],
				order["order_date"],
			),
		)
		cursor.execute(
			"DELETE FROM orders WHERE order_id = %s AND student_id = %s",
			(order_id, student_id),
		)
		connection.commit()
		return True
	except Exception:
		connection.rollback()
		raise
	finally:
		connection.close()


def restore_order(order_id, student_id):
	connection = get_connection()
	try:
		cursor = connection.cursor(dictionary=True)
		cursor.execute(
			"""
			SELECT order_id, student_id, service_id, copies, status, order_date
			FROM deleted_orders
			WHERE order_id = %s AND student_id = %s
			FOR UPDATE
			""",
			(order_id, student_id),
		)
		order = cursor.fetchone()
		if order is None:
			connection.rollback()
			return False

		cursor.execute(
			"""
			INSERT INTO orders
				(order_id, student_id, service_id, copies, status, order_date)
			VALUES (%s, %s, %s, %s, %s, %s)
			""",
			(
				order["order_id"],
				order["student_id"],
				order["service_id"],
				order["copies"],
				order["status"],
				order["order_date"],
			),
		)
		cursor.execute(
			"DELETE FROM deleted_orders WHERE order_id = %s AND student_id = %s",
			(order_id, student_id),
		)
		connection.commit()
		return True
	except Exception:
		connection.rollback()
		raise
	finally:
		connection.close()


def create_student(name, email, phone, password):
	connection = get_connection()
	try:
		cursor = connection.cursor()
		cursor.execute(
			"INSERT INTO students (name, email, phone, password) VALUES (%s, %s, %s, %s)",
			(name, email, phone or None, password),
		)
		connection.commit()
		return cursor.lastrowid
	finally:
		connection.close()


def update_order_status(order_id, status):
	connection = get_connection()
	try:
		cursor = connection.cursor(dictionary=True)
		cursor.execute(
			"""
			SELECT o.status, s.name, s.email
			FROM orders o
			JOIN students s ON s.student_id = o.student_id
			WHERE o.order_id = %s
			FOR UPDATE
			""",
			(order_id,),
		)
		order = cursor.fetchone()
		if order is None:
			connection.rollback()
			return None

		cursor.execute("UPDATE orders SET status = %s WHERE order_id = %s", (status, order_id))
		connection.commit()
		return order
	finally:
		connection.close()


__all__ = ["Error", "create_order", "create_student", "delete_order", "fetch_all", "fetch_one", "restore_order", "update_order_status"]
