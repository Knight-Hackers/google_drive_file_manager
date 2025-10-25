import React, { useState } from 'react';
import './LoginPage.css';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSignUp, setIsSignUp] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle login/signup logic here
    console.log('Form submitted:', { email, password, isSignUp });
  };

  return (
    <div className="login-page">
      <nav className="login-navbar">
        <div className="nav-container">
          <div className="logo">
            <span className="logo-icon">📂</span>
            <span className="logo-text">DriveViz</span>
          </div>
          <a href="/" className="back-home">← Back to Home</a>
        </div>
      </nav>

      <div className="login-container">
        <div className="login-content">
          <div className="login-visual">
            <div className="visual-card card-1">
              <div className="card-icon">🎓</div>
              <div className="card-text">School</div>
            </div>
            <div className="visual-card card-2">
              <div className="card-icon">💼</div>
              <div className="card-text">Work</div>
            </div>
            <div className="visual-card card-3">
              <div className="card-icon">🍳</div>
              <div className="card-text">Cooking</div>
            </div>
            <div className="visual-decoration circle-1"></div>
            <div className="visual-decoration circle-2"></div>
            <div className="visual-decoration circle-3"></div>
          </div>

          <div className="login-form-section">
            <div className="form-container">
              <h1 className="form-title">
                {isSignUp ? 'Create Account' : 'Welcome Back'}
              </h1>
              <p className="form-subtitle">
                {isSignUp 
                  ? 'Start organizing your Drive today' 
                  : 'Sign in to access your organized Drive'}
              </p>

              <button className="google-login-btn">
                <span className="google-icon-large">G</span>
                Continue with Google
              </button>

              <div className="divider">
                <span className="divider-text">or</span>
              </div>

              <div className="login-form">
                <div className="form-group">
                  <label htmlFor="email" className="form-label">Email</label>
                  <input
                    type="email"
                    id="email"
                    className="form-input"
                    placeholder="you@example.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="password" className="form-label">Password</label>
                  <input
                    type="password"
                    id="password"
                    className="form-input"
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                </div>

                {!isSignUp && (
                  <div className="form-options">
                    <label className="checkbox-label">
                      <input type="checkbox" />
                      <span>Remember me</span>
                    </label>
                    <a href="#" className="forgot-link">Forgot password?</a>
                  </div>
                )}

                <button onClick={handleSubmit} className="submit-btn">
                  {isSignUp ? 'Sign Up' : 'Sign In'}
                </button>
              </div>

              <div className="form-footer">
                <p>
                  {isSignUp ? 'Already have an account?' : "Don't have an account?"}
                  <button 
                    className="toggle-btn"
                    onClick={() => setIsSignUp(!isSignUp)}
                  >
                    {isSignUp ? 'Sign In' : 'Sign Up'}
                  </button>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;