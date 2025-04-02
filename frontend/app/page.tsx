"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import "./LandingPage.css";

export default function LandingPage() {
  const router = useRouter();

  return (
    <div className="landing-page">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <h1>CyberQuest</h1>
          <p className="hero-subtext">
            The ultimate platform to test and develop your skills in cybersecurity, AI, and competitive programming.
          </p>
          <div className="hero-buttons">
            <Link href="/register">
              <button className="btn primary">Join Now</button>
            </Link>
            <Link href="/login">
              <button className="btn secondary">Login</button>
            </Link>
          </div>
        </div>
      </section>

      {/* About Us */}
      <section className="about">
        <div className="section-content">
          <h2>About CyberQuest</h2>
          <p>
            CyberQuest is an advanced competition and learning platform designed for tech enthusiasts who want to master cybersecurity,
            artificial intelligence, and problem-solving. Our challenges are built to push the boundaries of your knowledge and skills.
          </p>
        </div>
      </section>

      {/* Challenges Section */}
      <section className="challenges">
        <div className="section-content">
          <h2>Start Your Challenge Journey</h2>
          <ul>
            <li><Link href="/level/1">Level 1: Digital Detective</Link></li>
            <li><Link href="/level/2">Level 2: Web Warriors</Link></li>
            <li><Link href="/level/3">Level 3: Cyber Heist</Link></li>
            <li><Link href="/level/4">Level 4: Malware Mayhem</Link></li>
            <li><Link href="/level/5">Level 5: Red Team vs Blue Team</Link></li>
          </ul>
        </div>
      </section>

      {/* Call to Action */}
      <section className="cta">
        <h2>Join the Future of Tech Challenges</h2>
        <p>Step up, compete, and sharpen your expertise in cybersecurity, AI, and software engineering.</p>
        <Link href="/register">
          <button className="btn primary">Get Started</button>
        </Link>
      </section>

      {/* Footer */}
      <footer className="footer">
        <p>&copy; 2025 CyberQuest. All Rights Reserved.</p>
      </footer>
    </div>
  );
}
