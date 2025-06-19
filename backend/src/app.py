from flask import Flask, jsonify, request
from flask_cors import CORS
from services.ipl_stats_service import IPLStatsService
import os

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

ipl_service = IPLStatsService()

DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), '../data/players.json')

@app.route('/api/players', methods=['GET'])
def get_players():
    # Automatically load from file if DB is empty
    if ipl_service.db.row_count() == 0:
        print("📂 No players in DB. Loading from file...")
        ipl_service.load_and_insert_data(DATA_FILE_PATH)

    team = request.args.get('team')
    role = request.args.get('role')
    if team:
        rows = ipl_service.get_players_by_team(team)
    elif role:
        rows = ipl_service.get_players_by_role(role)
    else:
        rows = ipl_service.get_all_players()

    columns = ['id', 'name', 'role', 'country', 'team', 'price']
    players = [dict(zip(columns, row)) for row in rows]
    return jsonify(players)

@app.route('/api/stats/basic', methods=['GET'])
def basic_stats():
    total_players, avg_price = ipl_service.basic_stats()
    return jsonify({'total_players': total_players, 'average_price': avg_price})

@app.route('/api/stats/teams', methods=['GET'])
def team_stats():
    return jsonify(ipl_service.team_analysis())

@app.route('/api/stats/roles', methods=['GET'])
def role_stats():
    return jsonify(ipl_service.role_analysis())

@app.route('/api/stats/countries', methods=['GET'])
def country_stats():
    return jsonify(ipl_service.country_analysis())

@app.route('/api/stats/advanced', methods=['GET'])
def advanced_stats():
    return jsonify(ipl_service.advanced_analysis())

@app.route('/api/stats/team-spending', methods=['GET'])
def team_spending():
    rows = ipl_service.get_team_spending()
    return jsonify([{"team": r[0], "total_price": r[1]} for r in rows])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
