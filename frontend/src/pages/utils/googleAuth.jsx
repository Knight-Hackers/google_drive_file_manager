// src/utils/googleAuth.js
export const handleGoogleLogin = () => {
  console.log('Google login initiated');
  window.location.href = "http://localhost:8000/user/login";
};