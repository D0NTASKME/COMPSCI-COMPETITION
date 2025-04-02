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

    const res = await fetch("http://127.0.0.1:8000/token", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formData,
    });

    const data = await res.json();
    if (res.ok) {
      localStorage.setItem("token", data.access_token);
      router.push("/dashboard");
    } else {
      setMessage("Invalid credentials.");
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-900 text-white">
      <div className="p-8 bg-gray-800 rounded-lg">
        <h1 className="text-2xl font-bold">Login</h1>
        <input
          className="mt-4 p-2 rounded-lg"
          placeholder="Username"
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          className="mt-4 p-2 rounded-lg"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
        />
        <button
          className="mt-4 p-2 bg-blue-600 text-white rounded-lg"
          onClick={handleLogin}
        >
          Login
        </button>
        {message && <p className="text-red-500 mt-2">{message}</p>}
      </div>
    </div>
  );
}
