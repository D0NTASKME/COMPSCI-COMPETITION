"use client";
import { useEffect, useState, useRef } from "react";
import { useRouter, useParams } from "next/navigation";
import { XMarkIcon, Bars3Icon, ArrowLeftIcon } from '@heroicons/react/24/outline';
import confetti from 'canvas-confetti';

interface ChallengeData {
  id: number;
  name: string;
  description: string;
  content?: string | null;
  image_url?: string | null;
  flag: string;
  xp_reward: number;
  hint?: string | null;
}

export default function Challenge() {
  const { challengeId } = useParams();
  const [challenge, setChallenge] = useState<ChallengeData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [submission, setSubmission] = useState("");
  const [submissionResult, setSubmissionResult] = useState<string | null>(null);
  const [hint, setHint] = useState<string | null>(null);
  const [hintCost] = useState(10); // Example hint cost
  const [remainingXp, setRemainingXp] = useState<number | null>(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const confettiCanvasRef = useRef<HTMLCanvasElement>(null); // To draw confetti on
  const [hasCompleted, setHasCompleted] = useState(false); // To track if the challenge is completed
  const router = useRouter();

  // Function to go back to the previous page (Level page)
  const goBack = () => {
    router.back();
  };

  useEffect(() => {
    const fetchChallenge = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`http://127.0.0.1:8000/challenges/${challengeId}`);
        if (!res.ok) {
          throw new Error(`Failed to fetch challenge: ${res.status}`);
        }
        const data = await res.json();
        setChallenge(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchChallenge();
    // Check if the user has already completed this challenge
    const checkCompletion = async () => {
      const token = localStorage.getItem("token");
      if (token && challengeId) {
        try {
          const res = await fetch(`http://127.0.0.1:8000/challenges/${challengeId}/status`, { // You'll need to create this backend route
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          if (res.ok) {
            const data = await res.json();
            setHasCompleted(data.completed);
            if (data.completed && confettiCanvasRef.current) {
              triggerConfetti(); // Show confetti if already completed
            }
          } else {
            console.error("Failed to check challenge completion status:", res);
          }
        } catch (error) {
          console.error("Error checking challenge completion status:", error);
        }
      }
    };
    checkCompletion();
  }, [challengeId]);

  useEffect(() => {
    if (submissionResult === "Challenge completed!") {
      setHasCompleted(true);
      triggerConfetti();
    }
  }, [submissionResult]);

  const triggerConfetti = () => {
    if (confettiCanvasRef.current) {
      const canvas = confettiCanvasRef.current;
      const jsConfetti = confetti.create(canvas, { resize: true });
      jsConfetti({
        particleCount: 200,
        spread: 70,
        origin: { y: 0.6 },
      });
    }
  };

  const handleFlagSubmit = async () => {
    if (!challenge || hasCompleted) return; // Don't allow submission if already completed
    setSubmissionResult(null);
    const token = localStorage.getItem("token");
    if (!token) {
      console.error("No token found, user is not authenticated.");
      setSubmissionResult("Not authenticated.");
      return;
    }
    try {
      const res = await fetch(`http://127.0.0.1:8000/challenges/${challenge.id}/submit_flag`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ flag: submission }),
      });
      const data = await res.json();
      if (res.ok) {
        setSubmissionResult(data.msg);
      } else {
        let errorMessage = "Submission failed.";
        if (data && typeof data === 'object' && data.detail) {
          errorMessage = data.detail;
        } else if (data && typeof data === 'object' && data.msg) {
          errorMessage = data.msg;
        } else if (typeof data === 'string') {
          errorMessage = data;
        } else {
          console.error("Unexpected error format:", data);
        }
        setSubmissionResult(errorMessage);
      }
    } catch (error: any) {
      setSubmissionResult("Error submitting flag.");
      console.error("Fetch error:", error);
    }
  };

  const handleGetHint = async () => {
    if (!challenge) return;
    setHint(null);
    const token = localStorage.getItem("token");
    if (!token) {
      console.error("No token found, user is not authenticated.");
      setHint("Not authenticated.");
      return;
    }
    try {
      const res = await fetch(`http://127.0.0.1:8000/challenges/${challenge.id}/hint`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      });
      const data = await res.json();
      if (res.ok && data.hint) {
        setHint(data.hint);
        setRemainingXp(data.remaining_xp);
      } else {
        let errorMessage = "Failed to get hint.";
        if (data && typeof data === 'object' && data.detail) {
          errorMessage = data.detail;
        } else if (data && typeof data === 'object' && data.msg) {
          errorMessage = data.msg;
        } else if (typeof data === 'string') {
          errorMessage = data;
        } else {
          console.error("Unexpected error format:", data);
        }
        setHint(errorMessage);
      }
    } catch (error: any) {
      setHint("Error getting hint.");
      console.error("Fetch error (hint):", error);
    }
  };

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  if (loading) {
    return <div>Loading challenge...</div>;
  }

  if (error) {
    return <div>Error loading challenge: {error}</div>;
  }

  if (!challenge) {
    return <div>Challenge not found.</div>;
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6 flex relative flex-col items-center">
      {hasCompleted && (
        <div className="fixed top-0 left-0 w-full bg-green-500 text-white p-4 text-center font-semibold z-10">
          🎉 Flag Successful! 🎉
        </div>
      )}
      <canvas ref={confettiCanvasRef} className="fixed top-0 left-0 w-full h-full pointer-events-none z-30"></canvas>
      {/* Back Button */}
      <button onClick={goBack} className="absolute top-4 left-4 bg-gray-800 text-white p-2 rounded hover:bg-gray-700 focus:outline-none z-40">
        <ArrowLeftIcon className="h-6 w-6" /> Back
      </button>
      {/* Main Challenge Content */}
      <div className={`w-full md:w-3/4 lg:w-1/2 ${hasCompleted ? 'mt-12' : 'mt-0'}`}> {/* Added conditional top margin */}
        <h1 className="text-3xl font-bold mb-4 text-center">{challenge.name}</h1>
        <p className="text-lg mb-6 text-center">Solve this cyber puzzle!</p>
        <div className="bg-gray-800 p-6 rounded-lg">
          {challenge.content && <div dangerouslySetInnerHTML={{ __html: challenge.content }} className="mb-4" />}
          {challenge.image_url && (
            <img
              src={challenge.image_url}
              alt={challenge.name}
              className="max-w-full rounded-md shadow-md mb-4"
            />
          )}
        </div>
        {!isSidebarOpen && (
          <button
            onClick={toggleSidebar}
            className="fixed top-4 right-4 bg-gray-800 text-white p-2 rounded hover:bg-gray-700 focus:outline-none"
          >
            <Bars3Icon className="h-6 w-6" />
          </button>
        )}
      </div>

      {/* Popup Sidebar */}
      <div
        className={`w-80 bg-gray-700 p-6 shadow-lg transform transition-transform duration-300 ${
          isSidebarOpen ? 'translate-x-0' : 'translate-x-full'
        } fixed top-0 right-0 h-full`}
      >
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-semibold">Challenge Brief</h2>
          <button onClick={toggleSidebar} className="text-gray-400 hover:text-white focus:outline-none">
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>
        <p className="mb-4">{challenge.description}</p>

        {/* Flag Submission */}
        <div>
          <h3 className="text-xl font-semibold mb-2">Submit Flag</h3>
          <input
            type="text"
            placeholder="FLAG{...}"
            className="w-full bg-gray-800 text-white rounded p-2 mb-2"
            value={submission}
            onChange={(e) => setSubmission(e.target.value)}
          />
          <button
            onClick={handleFlagSubmit}
            className="bg-green-600 text-white py-2 px-4 rounded hover:bg-green-700"
          >
            Submit
          </button>
          {submissionResult && submissionResult !== "Challenge completed!" && <p className={`mt-2 ${submissionResult === "Challenge completed!" ? "text-green-500" : "text-red-500"}`}>{submissionResult}</p>}
          {hasCompleted && <p className="mt-2 text-green-500">🎉 You've already completed this challenge! 🎉</p>}
        </div>

        {/* Hints */}
        <div className="mt-4">
          <h3 className="text-xl font-semibold mb-2">Hints</h3>
          <button
            onClick={handleGetHint}
            className="bg-yellow-500 text-white py-2 px-4 rounded hover:bg-yellow-600"
          >
            Get Hint (Costs {hintCost} XP)
          </button>
          {hint && <p className="mt-2 text-yellow-300">Hint: {hint}</p>}
          {remainingXp !== null && <p className="text-gray-400">Remaining XP after hint: {remainingXp}</p>}
        </div>
      </div>
    </div>
  );
}