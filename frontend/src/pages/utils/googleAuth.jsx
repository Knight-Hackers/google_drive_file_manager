// src/utils/googleAuth.js
export const handleGoogleLogin = () => {
  console.log('Google login initiated');
  window.location.href = "http://127.0.0.1:8000/user/login";
};