"""Crea una base SQLite de demostración a partir de los CSV originales."""

import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "pedidos_prueba.sqlite3"


def main():
    with sqlite3.connect(DB_PATH) as db:
        db.execute("PRAGMA foreign_keys=ON")
        db.execute("DROP TABLE IF EXISTS orders")
        db.execute("DROP TABLE IF EXISTS customers")
        db.execute(
            "CREATE TABLE customers "
            "(id INTEGER PRIMARY KEY, name TEXT, vip INTEGER, debt REAL)"
        )
        db.execute(
            "CREATE TABLE orders "
            "(id INTEGER PRIMARY KEY, customer_id INTEGER REFERENCES customers(id), "
            "total REAL, status TEXT)"
        )
        with (ROOT / "clientes_prueba.csv").open(encoding="utf-8-sig", newline="") as file:
            for row in csv.DictReader(file):
                db.execute(
                    "INSERT INTO customers VALUES (?,?,?,?)",
                    (
                        row["cliente_id"],
                        row["nombre_ficticio"],
                        row["es_vip"],
                        row["deuda"],
                    ),
                )
        with (ROOT / "pedidos_prueba.csv").open(encoding="utf-8-sig", newline="") as file:
            for row in csv.DictReader(file):
                db.execute(
                    "INSERT INTO orders VALUES (?,?,?,?)",
                    (
                        row["pedido_id"],
                        row["cliente_id"],
                        row["total"],
                        row["estado_inicial"],
                    ),
                )
    print("Base de demostración generada: pedidos_prueba.sqlite3")


if __name__ == "__main__":
    main()
