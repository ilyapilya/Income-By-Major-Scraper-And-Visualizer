import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [stats, setStats] = useState(null);
  const [plot, setPlot] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      // Fetch statistics
      const statsResponse = await axios.get('/api/statistics');
      setStats(statsResponse.data);

      // Fetch plot
      const plotResponse = await axios.get('/api/plot');
      setPlot(plotResponse.data.image);
    } catch (err) {
      setError(err.message || 'Failed to fetch data');
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="container loading">Loading data...</div>;
  }

  if (error) {
    return (
      <div className="container error">
        <h2>Error loading data</h2>
        <p>{error}</p>
        <button onClick={fetchData}>Retry</button>
      </div>
    );
  }

  return (
    <div className="container">
      <header className="header">
        <h1>College Major Income Analysis</h1>
        <p>Visualize median income by college major</p>
      </header>

      {stats && (
        <div className="statistics-grid">
          <div className="stat-card">
            <h3>Total Majors</h3>
            <p className="stat-value">{stats.total_majors}</p>
          </div>
          <div className="stat-card">
            <h3>Average Income</h3>
            <p className="stat-value">${stats.avg_income.toLocaleString()}</p>
          </div>
          <div className="stat-card">
            <h3>Highest Income</h3>
            <p className="stat-value">${stats.max_income.toLocaleString()}</p>
          </div>
          <div className="stat-card">
            <h3>Lowest Income</h3>
            <p className="stat-value">${stats.min_income.toLocaleString()}</p>
          </div>
        </div>
      )}

      {stats && stats.top_majors && (
        <div className="top-majors-section">
          <h2>Top 10 Highest Earning Majors</h2>
          <div className="top-majors-list">
            {stats.top_majors.map((major, index) => (
              <div key={index} className="top-major-item">
                <span className="rank">{index + 1}</span>
                <span className="major-name">{major.major}</span>
                <span className="major-income">${major.income.toLocaleString()}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {plot && (
        <div className="plot-section">
          <h2>Income Distribution by Major</h2>
          <img src={plot} alt="College Majors by Income" className="plot-image" />
        </div>
      )}

      <button className="refresh-btn" onClick={fetchData}>Refresh Data</button>
    </div>
  );
}

export default App;
