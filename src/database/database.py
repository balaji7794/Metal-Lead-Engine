import sqlite3
from pathlib import Path


class Database:

    def __init__(self):

        Path("database").mkdir(exist_ok=True)

        self.conn = sqlite3.connect("database/metal_leads.db")

        self.conn.row_factory = sqlite3.Row

        self.cursor = self.conn.cursor()

    def close(self):

        self.conn.close()