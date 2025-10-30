import React, { useState } from 'react';
import './LoginPage.css';
import { handleGoogleLogin } from './utils/googleAuth';

const LoginPage = () => {

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
              

              <button onClick={handleGoogleLogin} className="google-login-btn">
                <span className="google-icon-large">G</span>
                Sign In with Google
              </button>


            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;