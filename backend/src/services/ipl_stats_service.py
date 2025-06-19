import json
from services.database_service import PostgreSQLService

class IPLStatsService:
    def __init__(self):
        self.db = PostgreSQLService()
        self.db.create_table()

    def load_and_insert_data(self, json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)

        self.db.cursor.execute("SELECT COUNT(*) FROM players")
        existing = self.db.cursor.fetchone()[0]
        if existing < len(data):
            self.db.insert_players(data)
            print("✅ Players inserted into database")
        else:
            print(f"⚠️  Skipping data insert — {existing} rows already exist in DB.")

    def get_all_players(self):
        return self.db.fetch_all("SELECT * FROM players")

    def get_players_by_team(self, team):
        return self.db.fetch_all(f"SELECT * FROM players WHERE team = '{team}'")

    def get_players_by_role(self, role):
        return self.db.fetch_all(f"SELECT * FROM players WHERE role = '{role}'")

    def get_team_spending(self):
        return self.db.fetch_all("SELECT team, ROUND(SUM(price), 2) FROM players GROUP BY team ORDER BY SUM(price) DESC")

    def basic_stats(self):
        rows = self.db.fetch_all("SELECT COUNT(*) as total_players, ROUND(AVG(price), 2) as average_price FROM players")
        return rows[0] if rows else (0, 0.0)

    def team_analysis(self):
        return {
            "players_per_team": self.db.fetch_all("SELECT team, COUNT(*) FROM players GROUP BY team ORDER BY COUNT(*) DESC"),
            "total_value_per_team": self.db.fetch_all("SELECT team, ROUND(SUM(price), 2) FROM players GROUP BY team ORDER BY SUM(price) DESC"),
            "most_expensive_team": self.db.fetch_all("SELECT team, ROUND(SUM(price), 2) FROM players GROUP BY team ORDER BY SUM(price) DESC LIMIT 1")
        }

    def role_analysis(self):
        return {
            "players_per_role": self.db.fetch_all("SELECT role, COUNT(*) FROM players GROUP BY role ORDER BY COUNT(*) DESC"),
            "avg_price_per_role": self.db.fetch_all("SELECT role, ROUND(AVG(price), 2) FROM players GROUP BY role"),
            "most_expensive_role": self.db.fetch_all("SELECT role, ROUND(AVG(price), 2) FROM players GROUP BY role ORDER BY AVG(price) DESC LIMIT 1")
        }

    def country_analysis(self):
        return {
            "players_per_country": self.db.fetch_all("SELECT country, COUNT(*) FROM players GROUP BY country ORDER BY COUNT(*) DESC"),

            "most_expensive_player_per_country": self.db.fetch_all("SELECT DISTINCT ON (country) country, name, price FROM players ORDER BY country, price DESC")
        }

    def advanced_analysis(self):
        return {
            "top_5_expensive": self.db.fetch_all("SELECT name, price FROM players ORDER BY price DESC LIMIT 5"),
            "top_5_by_role": self.db.fetch_all("SELECT role, name, price FROM (SELECT *, RANK() OVER (PARTITION BY role ORDER BY price DESC) as rnk FROM players WHERE name IS NOT NULL) ranked WHERE rnk <= 5"),
            "top_5_by_team": self.db.fetch_all("SELECT team, name, price FROM (SELECT *, RANK() OVER (PARTITION BY team ORDER BY price DESC) as rnk FROM players WHERE name IS NOT NULL) ranked WHERE rnk <= 5"),
            "top_5_by_country": self.db.fetch_all("SELECT country, name, price FROM (SELECT *, RANK() OVER (PARTITION BY country ORDER BY price DESC) as rnk FROM players WHERE name IS NOT NULL) ranked WHERE rnk <= 5")
        }
