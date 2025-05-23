import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { toast } from "react-hot-toast";

export default function Home() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [userId, setUserId] = useState(null);

  // Check if we are in a local or production environment
  const backendUrl = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
    ? "http://127.0.0.1:8000"  // Use local URL for local development
    : "https://compsci-competition-backend.onrender.com";  // Use production URL for deployed frontend

  const registerUser = async () => {
    try {
      const res = await fetch(`${backendUrl}/register?username=${username}&email=${email}`, {
        method: "POST",
      });

      const data = await res.json();

      if (res.ok) {
        setUserId(data.user_id);
        toast.success("Registered successfully!");
      } else {
        toast.error("Registration failed");
      }
    } catch (error) {
      console.error("Error during registration:", error);
      toast.error("Something went wrong!");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <Card className="w-full max-w-md p-4">
        <CardContent>
          <h1 className="text-xl font-bold mb-4">Cyber AI Quantum Platform</h1>
          <Input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} className="mb-2" />
          <Input placeholder="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="mb-4" />
          <Button onClick={registerUser} className="w-full">Register</Button>
          {userId && <p className="mt-2 text-green-600">Registered! User ID: {userId}</p>}
        </CardContent>
      </Card>
    </div>
  );
}
