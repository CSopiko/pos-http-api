import sqlite3
from dataclasses import dataclass
from datetime import date
from typing import Dict

from app.core.manager import XReport
from app.core.receipt.interactor import Item, Receipt


@dataclass
class SqlitReceiptRepository:
    store_db: str = "store.db"
    max_rec_id: int = 0

    def __init__(self, store_db: str = "store.db") -> None:
        self.store_db = store_db
        with sqlite3.connect(self.store_db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS store
            (id INTEGER PRIMARY KEY, 
            item_id INTEGER UNIQUE ,
            item_name VARCHAR(30),
            item_price FLOAT );
            """
            )

            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS receipts
            (id INTEGER PRIMARY KEY,
            cashier_id INTEGER, 
            receipt_id INTEGER,
            item_id INTEGER,
            open_date TEXT,
            status BOOLEAN,
            FOREIGN KEY(item_id) REFERENCES store(item_id)
            );
            """
            )
            cursor.execute(
                """SELECT MAX(receipt_id)
            FROM receipts"""
            )
            res = cursor.fetchone()[0]
            self.max_rec_id = res if res is not None else 0

    def add_item_to_store(
        self, item_id: str, item_name: str, item_price: float
    ) -> None:
        with sqlite3.connect(self.store_db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO store(item_id, item_name, item_price)
            VALUES(?,?,?)""",
                (item_id, item_name, item_price),
            )

    def fetch_open_receipt(self, cashier_id: str) -> Receipt:
        with sqlite3.connect(self.store_db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT r.cashier_id, r.receipt_id, r.item_id, s.item_name, s.item_price
                 FROM receipts r 
                JOIN store s ON r.item_id=s.item_id
            WHERE r.cashier_id = (?)
            AND r.status=TRUE;""",
                (cashier_id),
            )
            rows = cursor.fetchall()
        cashier_id = ""
        receipt_id = ""
        item_list = []
        for r in rows:
            cashier_id = str(r[0])
            receipt_id = str(r[1])
            i = Item(item_id=r[2], item_name=r[3], item_price=r[4])
            item_list.append(i)
        return Receipt(cashier_id=cashier_id, receipt_id=receipt_id, items=item_list)

    def open_receipt(self, cashier_id: str) -> Receipt:
        self.max_rec_id += 1
        return Receipt(cashier_id=cashier_id, receipt_id=str(self.max_rec_id), items=[])

    def close_receipt(self, cashier_id: str) -> None:
        with sqlite3.connect(self.store_db) as conn:
            cursor = conn.cursor()

            today = date.today()
            d1 = today.strftime("%d/%m/%Y").replace("/", "")
            cursor.execute(
                """UPDATE receipts
            SET status = FALSE,
            open_date = (?)
            WHERE cashier_id = (?)
            AND status = TRUE
            """,
                (d1, cashier_id),
            )

    def add_item(self, item_id: str, cashier_id: str) -> None:
        with sqlite3.connect(self.store_db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT *
                FROM receipts 
                WHERE cashier_id=(?) 
                AND receipt_id=(?)
                AND status=FALSE """,
                (cashier_id, self.max_rec_id),
            )

            if cursor.fetchone() is not None:
                return

            cursor.execute(
                """INSERT INTO receipts (cashier_id, receipt_id, item_id, status)
            VALUES(?, ?, ?, ?)""",
                (cashier_id, self.max_rec_id, item_id, True),
            )

    def x_report(self, date: str) -> XReport:
        revenue: int = 0
        num_closed_receipts: int = 0
        sold_item_count: Dict[str, int] = {}
        # receipt , r_id- item1 3, item2 4
        with sqlite3.connect(self.store_db) as conn:
            cursor = conn.cursor()
            # today = date.today()
            # d1 = today.strftime("%d/%m/%Y")
            cursor.execute(
                """SELECT r.item_id, COUNT(r.item_id) FROM receipts r
            WHERE r.open_date=(?)
            AND r.status=FALSE
            GROUP BY r.item_id""",
                (date,),
            )
            for r in cursor.fetchall():
                sold_item_count[r[0]] = int(r[1])
            res = cursor.execute(
                """SELECT SUM(s.item_price) FROM receipts r
            LEFT JOIN store s ON r.item_id=s.item_id
            WHERE r.open_date=(?)
            AND r.status=FALSE
            """,
                (date,),
            )
            if res is not None:
                revenue = res.fetchone()[0]
            res = cursor.execute(
                """SELECT COUNT(DISTINCT r.receipt_id) FROM receipts r
            WHERE r.open_date=?
            AND r.status=FALSE;""",
                (date,),
            )
            if res is not None:
                num_closed_receipts = res.fetchone()[0]

        return XReport(
            revenue=revenue,
            num_closed_receipts=num_closed_receipts,
            sold_item_count=sold_item_count,
        )
