// components/Navbar.tsx
"use client";
import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="bg-gray-950 p-4 text-white">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Platform</h1>
        <div>
          <Link href="/" className="mr-4">
            Home
          </Link>
          <Link href="/register" className="mr-4">
            Register
          </Link>
          <Link href="/dashboard" className="mr-4">
            Dashboard
          </Link>
        </div>
      </div>
    </nav>
  );
}
