import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class PostgreSQLService:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        self.cursor = self.conn.cursor()
        print("✅ Connected to PostgreSQL")

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                name TEXT,
                role TEXT,
                country TEXT,
                team TEXT,
                price NUMERIC
            )
        ''')
        self.conn.commit()

    def insert_players(self, players):
        for player in players:
            self.cursor.execute('''
                INSERT INTO players (name, role, country, team, price)
                VALUES (%s, %s, %s, %s, %s)
            ''', (player['name'], player['role'], player['country'], player['team'], player['price']))
        self.conn.commit()

    def fetch_all(self, query):
        self.cursor.execute(query)
        if self.cursor.description:
            return self.cursor.fetchall()
        return []

    def close(self):
        self.cursor.close()
        self.conn.close()