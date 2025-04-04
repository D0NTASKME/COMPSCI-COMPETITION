"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link"; // Make sure to import the Link component

export default function Dashboard() {
  const [user, setUser] = useState({ username: "", email: "", xp: 0 });
  const [leaderboard, setLeaderboard] = useState<any[]>([]);
  const [levels, setLevels] = useState<any[]>([]); // Storing levels
  const [message, setMessage] = useState("");
  const router = useRouter();

  // Fetch user data and leaderboard data
  useEffect(() => {
    const fetchUserData = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        router.push("/login"); // Redirect if no token is found
        return;
      }

      const res = await fetch("https://compsci-competition-backend.onrender.com/users/profile", {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (res.ok) {
        const data = await res.json();
        setUser(data);
      } else {
        setMessage("Failed to fetch user data.");
      }
    };

    const fetchLeaderboard = async () => {
      const res = await fetch("https://compsci-competition-backend.onrender.com/users/leaderboard");
      if (res.ok) {
        const data = await res.json();
        setLeaderboard(data);
      } else {
        setMessage("Failed to fetch leaderboard.");
      }
    };

    const fetchLevels = async () => {
      const res = await fetch("https://compsci-competition-backend.onrender.com/levels");
      if (res.ok) {
        const data = await res.json();
        setLevels(data); // Setting levels from backend
      } else {
        setMessage("Failed to fetch levels."); // Updated message
      }
    };

    fetchUserData();
    fetchLeaderboard();
    fetchLevels(); // Fetching levels
  }, [router]);

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <h1 className="text-3xl font-bold mb-6">Welcome, {user.username}!</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Profile Card */}
        <div className="bg-gray-800 p-6 rounded-lg">
          <h2 className="text-xl font-bold">Profile</h2>
          <p>Email: {user.email}</p>
          <p>XP: {user.xp}</p>
        </div>

        {/* Leaderboard */}
        <div className="bg-gray-800 p-6 rounded-lg">
          <h2 className="text-xl font-bold">Leaderboard</h2>
          <ul>
            {leaderboard.map((player, index) => (
              <li key={index} className="flex justify-between">
                <span>{player.username}</span>
                <span>{player.xp} XP</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Challenges Section */}
        <div className="bg-gray-800 p-6 rounded-lg">
          <h2 className="text-xl font-bold">Challenges</h2>
          <ul>
            {levels.map((level) => (
              <li key={level.id}>
                <Link href={`/level/${level.id}`}> {/* Use the Link component here */}
                  <button className="text-white bg-blue-600 p-2 rounded hover:bg-blue-700">
                    {level.name} - {level.description}
                  </button>
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Feedback Message */}
      {message && <p className="mt-4 text-red-500">{message}</p>}
    </div>
  );
}