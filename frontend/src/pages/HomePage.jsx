import React, { useState } from 'react';
import { useNavigate, Link } from "react-router-dom";
import './HomePage.css';
import { handleGoogleLogin } from './utils/googleAuth';


// add button for heuristic or gemini approach
const HomePage = () => {
  const [isHovered, setIsHovered] = useState(false);
  const navigate = useNavigate();
  const features = [
    {
      icon: '📊',
      title: 'Smart Categorization',
      description: 'Automatically organize your files into intuitive categories',
      color: 'blue'
    },
    {
      icon: '🎨',
      title: 'Visual Overview',
      description: 'See your Drive in a beautiful, easy-to-navigate interface',
      color: 'red'
    },
    {
      icon: '🔍',
      title: 'Find Anything Fast',
      description: 'Quickly locate files by category instead of endless scrolling',
      color: 'yellow'
    },
    {
      icon: '🧹',
      title: 'Declutter Your Drive',
      description: 'Identify and manage clutter with smart insights',
      color: 'green'
    }
  ];

  const categories = [
    { name: 'School', icon: '🎓', count: 124, color: 'blue' },
    { name: 'Work', icon: '💼', count: 89, color: 'red' },
    { name: 'Cooking', icon: '🍳', count: 34, color: 'yellow' },
    { name: 'Photos', icon: '📸', count: 456, color: 'green' },
    { name: 'Music', icon: '🎵', count: 78, color: 'purple' },
    { name: 'Other', icon: '📁', count: 203, color: 'blue' }
  ];

  return (
    <div className="homepage">
      <nav className="navbar">
        <div className="nav-container">
          <div className="logo">
            <span className="logo-icon">📂</span>
            <span className="logo-text">DriveViz</span>
          </div>
          <div className="nav-links">
            <button className="sign-in-button" onClick={() => navigate("/login")}>Sign In</button>
          </div>
        </div>
      </nav>

      <section className="hero">
        <div className="hero-content">
          <h1 className="hero-title">
            Visualize Your Google Drive
            <span className="title-accent"> Like Never Before</span>
          </h1>
          <p className="hero-subtitle">
            Transform chaos into clarity. Organize, visualize, and navigate your files with intelligent categorization.
          </p>
          <button 
            className="cta-button"
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
            onClick={handleGoogleLogin}
          >
            <span className="google-icon">G</span>
            Connect Google Drive
          </button>
          <p className="hero-note">Free to use • No credit card required</p>
        </div>
        
        <div className="hero-visual">
          <div className="drive-preview">
            <div className="preview-header">
              <div className="preview-dots">
                <span className="dot red"></span>
                <span className="dot yellow"></span>
                <span className="dot green"></span>
              </div>
              <div className="preview-title">My Drive</div>
            </div>
            <div className="category-grid">
              {categories.map((cat, idx) => (
                <div key={idx} className={`category-card ${cat.color}`}>
                  <div className="category-icon">{cat.icon}</div>
                  <div className="category-name">{cat.name}</div>
                  <div className="category-count">{cat.count} files</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="features" id="features">
        <div className="features-container">
          <h2 className="section-title">Everything You Need</h2>
          <p className="section-subtitle">Powerful features to make your Drive work for you</p>
          
          <div className="features-grid">
            {features.map((feature, idx) => (
              <div key={idx} className={`feature-card ${feature.color}`}>
                <div className="feature-icon">{feature.icon}</div>
                <h3 className="feature-title">{feature.title}</h3>
                <p className="feature-description">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="how-it-works" id="how-it-works">
        <div className="how-container">
          <h2 className="section-title">How It Works</h2>
          <div className="steps">
            <div className="step">
              <div className="step-number blue">1</div>
              <h3 className="step-title">Connect Your Drive</h3>
              <p className="step-description">Securely link your Google Drive account in seconds</p>
            </div>
            <div className="step-arrow">→</div>
            <div className="step">
              <div className="step-number red">2</div>
              <h3 className="step-title">Smart Analysis</h3>
              <p className="step-description">Our AI categorizes your files intelligently</p>
            </div>
            <div className="step-arrow">→</div>
            <div className="step">
              <div className="step-number green">3</div>
              <h3 className="step-title">Explore & Organize</h3>
              <p className="step-description">Browse by category and stay organized effortlessly</p>
            </div>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <div className="cta-content">
          <h2 className="cta-title">Ready to Transform Your Drive?</h2>
          <p className="cta-text">Join thousands of users who've already discovered a better way to manage their files.</p>
          <button onClick={handleGoogleLogin} className="cta-button-large">
            <span className="google-icon">G</span>
            Get Started Now
          </button>
        </div>
      </section>

      <footer className="footer">
        <div className="footer-content">
          <div className="footer-section">
            <div className="footer-logo">
              <span className="logo-icon">📂</span>
              <span className="logo-text">DriveViz</span>
            </div>
            <p className="footer-description">Making Google Drive beautiful and organized.</p>
          </div>
          <div className="footer-section">
            <h4 className="footer-heading">Product</h4>
            <a href="#" className="footer-link">Features</a>
            <a href="#" className="footer-link">Pricing</a>
            <a href="#" className="footer-link">Security</a>
          </div>
          <div className="footer-section">
            <h4 className="footer-heading">Company</h4>
            <a href="#" className="footer-link">About</a>
            <a href="#" className="footer-link">Blog</a>
            <a href="#" className="footer-link">Contact</a>
          </div>
          <div className="footer-section">
            <h4 className="footer-heading">Legal</h4>
            <a href="#" className="footer-link">Privacy</a>
            <a href="#" className="footer-link">Terms</a>
          </div>
        </div>
        <div className="footer-bottom">
          <p>© 2025 DriveViz. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;