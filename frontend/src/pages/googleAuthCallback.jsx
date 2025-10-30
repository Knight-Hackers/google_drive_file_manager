import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const GoogleCallbackPage = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // If backend returns token in query params
    const params = new URLSearchParams(window.location.search);
    const accessToken = params.get('access_token');

    if (accessToken) {
      localStorage.setItem('access_token', accessToken);
      navigate('/dashboard'); // redirect to your main page
    }
  }, [navigate]);

  return <div>Logging you in...</div>;
};

export default GoogleCallbackPage;
