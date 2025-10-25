const DashboardPage = () => {
  const token = localStorage.getItem('googleAccessToken');

  useEffect(() => {
    if (token) {
      fetch('http://127.0.0.1:8000/files/list', {
        headers: { Authorization: `Bearer ${token}` }
      })
        .then(res => res.json())
        .then(data => console.log(data));
    }
  }, [token]);

  return <div>Welcome to your Drive dashboard!</div>;
};

export default DashboardPage;