"use client"

import Link from "next/link"
import { useEffect, useRef } from "react"

export default function LandingPage() {
  const observerRef = useRef<IntersectionObserver | null>(null)

  useEffect(() => {
    const observerOptions = {
      threshold: 0.1,
      rootMargin: "0px 0px -50px 0px",
    }

    observerRef.current = new IntersectionObserver((entries) => {
      entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
          setTimeout(() => {
            entry.target.classList.add("active")
          }, index * 100)
        }
      })
    }, observerOptions)

    const reveals = document.querySelectorAll(".scroll-reveal")
    reveals.forEach((el) => observerRef.current?.observe(el))

    return () => {
      if (observerRef.current) {
        observerRef.current.disconnect()
      }
    }
  }, [])

  return (
    <div className="landing-page">
            {/* Navigation */}
      <nav className="navbar">
        <div className="nav-container">
          <Link href="/" className="logo">
            MailFit
          </Link>
          <div className="nav-buttons">
            <Link href="/login" className="btn-signin">
              Sign In
            </Link>
            <Link href="/sign-up" className="btn-signup">
              Sign Up
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero">
        <div className="blob blob-1"></div>
        <div className="blob blob-2"></div>
        <div className="container hero-content">
          <h1>
            Your job emails should <span className="highlight">actually fit</span> the
            job
          </h1>
          <p className="tagline">
            Stop sending generic applications. Start landing interviews.
          </p>
          <Link href="/signup" className="cta-button">
            Try MailFit Free
          </Link>
        </div>
      </section>

      {/* Problem Section */}
      <section className="problem-section">
        <div className="container">
          <h2 className="section-title scroll-reveal">
            The Real Problem Isn&apos;t Writing
          </h2>
          <div className="problem-cards">
            <div className="problem-card scroll-reveal">
              <span className="problem-emoji">😴</span>
              <h3>Generic = Ignored</h3>
              <p>
                Recruiters spot copy-paste emails instantly. Generic wording kills
                your response rate before they even read your resume.
              </p>
            </div>
            <div className="problem-card scroll-reveal">
              <span className="problem-emoji">⏰</span>
              <h3>Customizing Takes Forever</h3>
              <p>
                Tailoring each email takes 15-30 minutes. When you&apos;re applying to
                10+ roles, that&apos;s an entire workday lost.
              </p>
            </div>
            <div className="problem-card scroll-reveal">
              <span className="problem-emoji">🤖</span>
              <h3>AI Tools Miss Context</h3>
              <p>
                Most AI writes fluent text but doesn&apos;t understand job requirements,
                role expectations, or skill alignment.
              </p>
            </div>
          </div>
          <div className="problem-highlight">
            <p>
              The pain isn&apos;t writing English. It&apos;s writing <em>relevance</em>.
            </p>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="how-section">
        <div className="container">
          <h2 className="section-title" style={{ color: "white" }}>
            How MailFit Actually Works
          </h2>
          <div className="steps">
            <div className="step scroll-reveal">
              <div className="step-number">01</div>
              <div className="step-content">
                <h3>Paste the Job Description</h3>
                <p>
                  Just copy-paste any job posting. MailFit reads the entire thing -
                  skills, responsibilities, company culture, everything.
                </p>
              </div>
            </div>
            <div className="step scroll-reveal">
              <div className="step-number">02</div>
              <div className="step-content">
                <h3>MailFit Analyzes Context</h3>
                <p>
                  We extract what recruiters actually care about: required skills,
                  seniority level, team structure, and company tone. No guesswork.
                </p>
              </div>
            </div>
            <div className="step scroll-reveal">
              <div className="step-number">03</div>
              <div className="step-content">
                <h3>Get Your Role-Aligned Email</h3>
                <p>
                  Receive a professional, contextual email written specifically for
                  THIS job. Not a template. An email that fits.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Why Not ChatGPT */}
      <section className="comparison-section">
        <div className="container">
          <h2 className="section-title scroll-reveal">Why Not Just Use ChatGPT?</h2>
          <div className="comparison-box scroll-reveal">
            <h3>MailFit is specialized for job applications</h3>
            <ul className="comparison-list">
              <li>Focuses on job-specific context, not generic text generation</li>
              <li>Produces structured, recruiter-friendly emails every time</li>
              <li>Avoids generic phrasing that screams &quot;AI-written&quot;</li>
              <li>Maintains consistent professional tone across all applications</li>
              <li>Understands what recruiters look for in emails</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Who This Is For */}
      <section className="audience-section">
        <div className="container">
          <h2 className="section-title scroll-reveal">
            Built For Job Seekers Like You
          </h2>
          <div className="audience-grid">
            <div className="audience-card scroll-reveal">
              <span className="icon">👩‍💻</span>
              <h3>Developers & Engineers</h3>
              <p>You know your code is solid. Now make sure your emails reflect that.</p>
            </div>
            <div className="audience-card scroll-reveal">
              <span className="icon">🚀</span>
              <h3>Multi-Role Applicants</h3>
              <p>
                Applying to 20 roles? Don&apos;t waste 10 hours writing emails. Let MailFit
                do it.
              </p>
            </div>
            <div className="audience-card scroll-reveal">
              <span className="icon">✨</span>
              <h3>Quality-Focused Candidates</h3>
              <p>
                You want every application to feel intentional, not rushed. We get it.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Stats/Outcomes */}
      <section className="stats-section">
        <div className="container">
          <h2 className="section-title scroll-reveal" style={{ color: "white" }}>
            What You&apos;ll Get
          </h2>
          <div className="stats-grid">
            <div className="scroll-reveal">
              <div className="stat-number">90%</div>
              <div className="stat-label">Less time writing</div>
            </div>
            <div className="scroll-reveal">
              <div className="stat-number">3x</div>
              <div className="stat-label">Higher quality</div>
            </div>
            <div className="scroll-reveal">
              <div className="stat-number">100%</div>
              <div className="stat-label">More confidence</div>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="cta-section">
        <div className="container">
          <h2 className="scroll-reveal">Stop Wasting Time on Generic Emails</h2>
          <p className="scroll-reveal">
            Turn job descriptions into relevant, professional emails in seconds.
          </p>
          <Link href="/signup" className="cta-large scroll-reveal">
            Get Started Free
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer>
        <div className="container">
          <p>
            &copy; 2026 MailFit. Helping job seekers land interviews, not spam folders.
          </p>
        </div>
      </footer>
    </div>
  )
}