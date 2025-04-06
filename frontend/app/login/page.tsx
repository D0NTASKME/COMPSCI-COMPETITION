"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const router = useRouter();

  const handleLogin = async () => {
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    try {
      // Perform the fetch request to the backend API
      const res = await fetch("https://compsci-competition-backend.onrender.com/token", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData,
      });

      // Check if the response is not ok (i.e., error in response)
      if (!res.ok) {
        throw new Error('Failed to authenticate');
      }

      // Parse the response data
      const data = await res.json();
      console.log("Response Data:", data); // Log to inspect the response

      // Store the token if authentication is successful
      localStorage.setItem("token", data.access_token);

      // Redirect to the dashboard
      router.push("/dashboard");
    } catch (error) {
      console.error('Login Error:', error); // Log any errors
      setMessage("Invalid credentials.");
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-900 text-white">
      <div className="p-8 bg-gray-800 rounded-lg">
        <h1 className="text-2xl font-bold">Login</h1>
        
        {/* Username input */}
        <input
          className="mt-4 p-2 rounded-lg"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        {/* Password input */}
        <input
          type="password"
          className="mt-4 p-2 rounded-lg"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {/* Login button */}
        <button
          className="mt-4 p-2 bg-blue-600 text-white rounded-lg"
          onClick={handleLogin}
        >
          Login
        </button>

        {/* Error message if login fails */}
        {message && <p className="text-red-500 mt-2">{message}</p>}
      </div>
    </div>
  );
}
