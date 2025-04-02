"use client";
import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation"; // Import useParams
import Link from "next/link";

interface Challenge {
  id: number;
  name: string;
  description: string;
}

interface LevelData {
  id: number;
  name: string;
  description: string | null;
  order: number;
}

export default function Level() { // Remove params from the function definition
  const { levelId } = useParams(); // Use the useParams hook to get levelId
  const [level, setLevel] = useState<LevelData | null>(null);
  const [challenges, setChallenges] = useState<Challenge[]>([]);
  const [completedChallenges, setCompletedChallenges] = useState<number[]>([]);
  const [message, setMessage] = useState("");
  const router = useRouter();

  useEffect(() => {
    const fetchLevelData = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          setMessage("You need to be logged in to see your progress!");
          return;
        }

        const levelRes = await fetch(`http://127.0.0.1:8000/levels/${levelId}`);
        if (!levelRes.ok) throw new Error("Oops! Failed to get the level info.");
        const levelData = await levelRes.json();
        setLevel(levelData);

        const challengesRes = await fetch(`http://127.0.0.1:8000/levels/${levelId}/challenges`);
        if (!challengesRes.ok) throw new Error("Uh oh! Couldn't load the challenges for this level.");
        const challengesData = await challengesRes.json();
        setChallenges(challengesData);

        // Fetch the challenges you've already finished for this level
        const completedRes = await fetch(
          `http://127.0.0.1:8000/users/completed_challenges?level_id=${levelId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        if (completedRes.ok) {
          const completedData = await completedRes.json();
          setCompletedChallenges(completedData.completed_challenge_ids);
        } else {
          console.error("Failed to fetch completed challenges:", completedRes);
          setMessage("Hmm, couldn't load which challenges you've finished.");
        }

      } catch (error) {
        setMessage(error instanceof Error ? error.message : "Something went wrong while loading the level.");
      }
    };

    if (levelId) {
      fetchLevelData();
    }
  }, [levelId]);

  const getChallengeStatusIcon = (challengeId: number) => {
    if (completedChallenges.includes(challengeId)) {
      return "✅"; // Green checkmark for completed!
    }
    return "🔓"; // Open lock for not yet done
  };

  if (!level) {
    return <div>Loading level data... just a sec!</div>;
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <h1 className="text-3xl font-bold mb-6">{level.name}</h1>
      <p className="mb-4">{level.description}</p>

      <h2 className="text-2xl font-semibold mb-4">Available Challenges</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {challenges.map((challenge) => (
          <div key={challenge.id} className="bg-gray-800 p-4 rounded-lg">
            <Link href={`/challenge/${challenge.id}`}>
              <div className="flex items-center justify-between">
                <h3 className="text-xl font-bold mb-2">{challenge.name}</h3>
                <span className="text-xl">{getChallengeStatusIcon(challenge.id)}</span>
              </div>
              <p className="text-gray-400">{challenge.description.substring(0, 100)}...</p>
            </Link>
          </div>
        ))}
      </div>

      {message && <p className="mt-4 text-red-500">{message}</p>}
    </div>
  );
}