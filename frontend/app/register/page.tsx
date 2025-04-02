"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const router = useRouter();

  const handleRegister = async () => {
    const res = await fetch("http://127.0.0.1:8000/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password }),
    });

    const data = await res.json();
    if (res.ok) {
      // Ensure the backend responds with a token (adjust the backend if necessary)
      localStorage.setItem("token", data.access_token);
      router.push("/dashboard");  // Navigate to dashboard after successful registration
    } else {
      // Handling errors from the backend
      setMessage(`Error: ${data.detail || "Something went wrong"}`);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-900 text-white">
      <div className="p-8 bg-gray-800 rounded-lg">
        <h1 className="text-2xl font-bold">Register</h1>
        <input
          type="text"
          placeholder="Username"
          className="mb-4 p-2 rounded"
          onChange={(e) => setUsername(e.target.value)}
          value={username}
        />
        <input
          type="email"
          placeholder="Email"
          className="mb-4 p-2 rounded"
          onChange={(e) => setEmail(e.target.value)}
          value={email}
        />
        <input
          type="password"
          placeholder="Password"
          className="mb-4 p-2 rounded"
          onChange={(e) => setPassword(e.target.value)}
          value={password}
        />
        <button
          className="w-full p-2 bg-blue-600 hover:bg-blue-700 rounded text-white"
          onClick={handleRegister}
        >
          Register
        </button>
        {message && <p className="mt-4 text-red-500">{message}</p>}
      </div>
    </div>
  );
}
