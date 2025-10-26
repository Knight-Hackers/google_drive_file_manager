// src/pages/DashboardPage.jsx
import { useEffect, useState } from 'react';

const DashboardPage = () => {
  const token = localStorage.getItem('access_token');
  const [files, setFiles] = useState([]);
  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    if (!token) return;

    // Fetch file list
    //fetch('http://127.0.0.1:8000/files/list', {
      //headers: { Authorization: `Bearer ${token}` },
    //})
      //.then(res => res.json())
      //.then(data => setFiles(data.files))
      //.catch(err => console.error('Error fetching files:', err));

    // Fetch categorized/analysis
    fetch('http://127.0.0.1:8000/files/analyze/heuristic', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(res => res.json())
      .then(data => setAnalysis(data))
      .catch(err => console.error('Error analyzing files:', err));
  }, [token]);

  if (!token) {
    return <div>Please log in first.</div>;
  }

  return (
    <div>
      <h1>Welcome to your Drive Dashboard!</h1>

      <h2>Analysis</h2>
      {analysis ? (
        <div>
          <p>Total files: {analysis.total_files}</p>
          <ul>
            {Object.entries(analysis.categories).map(([category, count]) => (
              <li key={category}>
                {category}: {count}
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <p>Analyzing files...</p>
      )}
    </div>
  );
};

export default DashboardPage;
