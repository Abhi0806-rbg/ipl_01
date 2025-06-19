// App.jsx
import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";
import "./App.css"; // Assuming you have some basic styles in App.css
const COLORS = ["#34d399", "#60a5fa", "#facc15", "#f87171", "#a78bfa"];

const App = () => {
  const [basic, setBasic] = useState({});
  const [teams, setTeams] = useState({});
  const [advanced, setAdvanced] = useState({});
  const [roles, setRoles] = useState({});
  // const [countries, setCountries] = useState([]);
  const [teamSpending, setTeamSpending] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5050/api/stats/basic").then((r) => r.json()).then(setBasic);
    fetch("http://localhost:5050/api/stats/teams").then((r) => r.json()).then(setTeams);
    fetch("http://localhost:5050/api/stats/advanced").then((r) => r.json()).then(setAdvanced);
    fetch("http://localhost:5050/api/stats/roles").then((r) => r.json()).then(setRoles);
    // fetch("http://localhost:5050/api/stats/countries").then((r) => r.json()).then(setCountries);
    fetch("http://localhost:5050/api/stats/team-spending").then((r) => r.json()).then(setTeamSpending);
  }, []);

  const roleData = (roles.players_per_role || []).map(([role, count], ) => ({
    name: role,
    value: count,
  }));

  const teamSpendingData = (teamSpending || []).map(({ team, total_price }) => ({
    name: team,
    value: total_price,
  }));

  return (
    <div className="min-h-screen p-6 bg-gradient-to-br from-slate-900 to-gray-950 text-white">
      <h1 className="text-4xl font-bold text-center mb-8 bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600">
        IPL Statistics Hub
      </h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard title="Total Auction Value" value={`₹${(teams.total_value_per_team?.reduce((a, b) => a + parseFloat(b[1]), 0) || 0).toFixed(1)} Cr`} />
        <StatCard title="Average Player Price" value={`₹${basic.average_price || 0} Cr`} />
        <StatCard title="Total Players" value={basic.total_players || 0} />
        <StatCard title="Highest Bid" value={`₹${advanced.top_5_expensive?.[0]?.price || 0} Cr`} />
      </div>

      <div className="grid md:grid-cols-2 gap-6 mb-12">
        <div className="bg-white/10 p-4 rounded-xl">
          <h2 className="text-lg font-semibold mb-4">Team Spending Comparison</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={teamSpendingData}>
              <XAxis dataKey="name" stroke="#fff" />
              <YAxis stroke="#fff" />
              <Tooltip />
              <Bar dataKey="value" fill="#60a5fa" barSize={30} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white/10 p-4 rounded-xl">
          <h2 className="text-lg font-semibold mb-4">Player Role Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={roleData}
                cx="50%"
                cy="50%"
                labelLine={false}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {roleData.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white/10 p-4 rounded-xl">
          <h2 className="text-lg font-semibold mb-4">Most Expensive Players</h2>
          <ol className="list-decimal ml-6">
            {(advanced.top_5_expensive || []).map((p, i) => (
              <li key={i} className="mb-2">{p.name} - ₹{p.price} Cr</li>
            ))}
          </ol>
        </div>

        <div className="bg-white/10 p-4 rounded-xl">
          <h2 className="text-lg font-semibold mb-4">Top 5 by Role</h2>
          <ol className="list-decimal ml-6">
            {(advanced.top_5_by_role || []).map((p, i) => (
              <li key={i} className="mb-2">{p.role}: {p.name} - ₹{p.price} Cr</li>
            ))}
          </ol>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ title, value }) => (
  <div className="glass text-center">
    <div className="text-sm text-gray-300 mb-1">{title}</div>
    <div className="text-2xl font-bold text-white">{value}</div>
  </div>
);

export default App;
