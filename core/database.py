# core/database.py

import sqlite3
import threading
from datetime import datetime


# =========================================================
# DATABASE FILE
# =========================================================

DATABASE_FILE = "tsnova.db"


# =========================================================
# DATABASE MANAGER
# =========================================================

class DatabaseManager:

    def __init__(self):

        self.connection = None

        self.lock = threading.Lock()

        self.connect()

        self.create_tables()

    # =====================================================
    # CONNECT
    # =====================================================

    def connect(self):

        try:

            self.connection = sqlite3.connect(

                DATABASE_FILE,

                check_same_thread=False
            )

            self.connection.row_factory = (
                sqlite3.Row
            )

            print(
                "Database connected"
            )

        except Exception as error:

            print(
                f"Database Connect Error: {error}"
            )

    # =====================================================
    # CREATE TABLES
    # =====================================================

    def create_tables(self):

        try:

            with self.lock:

                cursor = self.connection.cursor()

                # =========================================
                # TASKS TABLE
                # =========================================

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS tasks (

                        id INTEGER PRIMARY KEY AUTOINCREMENT,

                        input_path TEXT NOT NULL,

                        output_path TEXT,

                        status TEXT DEFAULT 'waiting',

                        progress INTEGER DEFAULT 0,

                        model_name TEXT,

                        retry_count INTEGER DEFAULT 0,

                        created_at TEXT,

                        updated_at TEXT
                    )
                    """
                )

                self.connection.commit()

                print(
                    "Database tables ready"
                )

        except Exception as error:

            print(
                f"Create Tables Error: {error}"
            )

    # =====================================================
    # CREATE TASK
    # =====================================================

    def create_task(

        self,

        input_path,

        output_path="",

        model_name=""
    ):

        try:

            with self.lock:

                cursor = self.connection.cursor()

                timestamp = (
                    datetime.now().isoformat()
                )

                cursor.execute(
                    """
                    INSERT INTO tasks (

                        input_path,
                        output_path,
                        status,
                        progress,
                        model_name,
                        retry_count,
                        created_at,
                        updated_at

                    )

                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,

                    (
                        input_path,
                        output_path,
                        "waiting",
                        0,
                        model_name,
                        0,
                        timestamp,
                        timestamp
                    )
                )

                self.connection.commit()

                return cursor.lastrowid

        except Exception as error:

            print(
                f"Create Task Error: {error}"
            )

            return None

    # =====================================================
    # UPDATE TASK STATUS
    # =====================================================

    def update_task_status(

        self,

        input_path,

        status
    ):

        try:

            with self.lock:

                cursor = self.connection.cursor()

                cursor.execute(
                    """
                    UPDATE tasks

                    SET
                        status = ?,
                        updated_at = ?

                    WHERE input_path = ?
                    """,

                    (
                        status,
                        datetime.now().isoformat(),
                        input_path
                    )
                )

                self.connection.commit()

        except Exception as error:

            print(
                f"Update Status Error: {error}"
            )

    # =====================================================
    # UPDATE TASK PROGRESS
    # =====================================================

    def update_task_progress(

        self,

        input_path,

        progress
    ):

        try:

            with self.lock:

                cursor = self.connection.cursor()

                cursor.execute(
                    """
                    UPDATE tasks

                    SET
                        progress = ?,
                        updated_at = ?

                    WHERE input_path = ?
                    """,

                    (
                        progress,
                        datetime.now().isoformat(),
                        input_path
                    )
                )

                self.connection.commit()

        except Exception as error:

            print(
                f"Update Progress Error: {error}"
            )

    # =====================================================
    # UPDATE OUTPUT PATH
    # =====================================================

    def update_output_path(

        self,

        input_path,

        output_path
    ):

        try:

            with self.lock:

                cursor = self.connection.cursor()

                cursor.execute(
                    """
                    UPDATE tasks

                    SET
                        output_path = ?,
                        updated_at = ?

                    WHERE input_path = ?
                    """,

                    (
                        output_path,
                        datetime.now().isoformat(),
                        input_path
                    )
                )

                self.connection.commit()

        except Exception as error:

            print(
                f"Update Output Error: {error}"
            )

    # =====================================================
    # INCREMENT RETRY
    # =====================================================

    def increment_retry_count(
        self,
        input_path
    ):

        try:

            with self.lock:

                cursor = self.connection.cursor()

                cursor.execute(
                    """
                    UPDATE tasks

                    SET
                        retry_count = retry_count + 1,
                        updated_at = ?

                    WHERE input_path = ?
                    """,

                    (
                        datetime.now().isoformat(),
                        input_path
                    )
                )

                self.connection.commit()

        except Exception as error:

            print(
                f"Retry Count Error: {error}"
            )

    # =====================================================
    # GET TASK
    # =====================================================

    def get_task(
        self,
        input_path
    ):

        try:

            with self.lock:

                cursor = self.connection.cursor()

                cursor.execute(
                    """
                    SELECT *

                    FROM tasks

                    WHERE input_path = ?
                    """,

                    (input_path,)
                )

                result = cursor.fetchone()

                if result:

                    return dict(result)

                return None

        except Exception as error:

            print(
                f"Get Task Error: {error}"
            )

            return None

    # =====================================================
    # GET ALL TASKS
    # =====================================================

    def get_all_tasks(self):

        try:

            with self.lock:

                cursor = self.connection.cursor()

                cursor.execute(
                    """
                    SELECT *

                    FROM tasks

                    ORDER BY id DESC
                    """
                )

                results = cursor.fetchall()

                return [

                    dict(row)

                    for row in results
                ]

        except Exception as error:

            print(
                f"Get All Tasks Error: {error}"
            )

            return []

    # =====================================================
    # GET TASKS BY STATUS
    # =====================================================

    def get_tasks_by_status(
        self,
        status
    ):

        try:

            with self.lock:

                cursor = self.connection.cursor()

                cursor.execute(
                    """
                    SELECT *

                    FROM tasks

                    WHERE status = ?
                    """,

                    (status,)
                )

                results = cursor.fetchall()

                return [

                    dict(row)

                    for row in results
                ]

        except Exception as error:

            print(
                f"Get Tasks By Status Error: {error}"
            )

            return []

    # =====================================================
    # DELETE TASK
    # =====================================================

    def delete_task(
        self,
        input_path
    ):

        try:

            with self.lock:

                cursor = self.connection.cursor()

                cursor.execute(
                    """
                    DELETE FROM tasks

                    WHERE input_path = ?
                    """,

                    (input_path,)
                )

                self.connection.commit()

        except Exception as error:

            print(
                f"Delete Task Error: {error}"
            )

    # =====================================================
    # CLEAR TASKS
    # =====================================================

    def clear_tasks(self):

        try:

            with self.lock:

                cursor = self.connection.cursor()

                cursor.execute(
                    """
                    DELETE FROM tasks
                    """
                )

                self.connection.commit()

        except Exception as error:

            print(
                f"Clear Tasks Error: {error}"
            )

    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):

        try:

            if self.connection:

                self.connection.close()

                print(
                    "Database closed"
                )

        except Exception as error:

            print(
                f"Database Close Error: {error}"
            )

    # =====================================================
    # GET UNFINISHED TASKS
    # =====================================================

    def get_unfinished_tasks(self):

        try:

            with self.lock:

                cursor = self.connection.cursor()

                cursor.execute(
                    """
                    SELECT *

                    FROM tasks

                    WHERE status IN (
                        'waiting',
                        'processing'
                    )
                    """
                )

                results = cursor.fetchall()

                return [

                    dict(row)

                    for row in results
                ]

        except Exception as error:

            print(
                f"Get Unfinished Tasks Error: {error}"
            )

            return []

# =========================================================
# GLOBAL INSTANCE
# =========================================================

database_manager = DatabaseManager()