import { useEffect, useState } from 'react';
import './App.css';
import spinner from './load-icon.png'; // Make sure this image exists

function App() {
  const [loading, setLoading] = useState(true);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(false);
  const [responseData, setResponseData] = useState(null);

  useEffect(() => {
    fetch('http://34.29.111.224:5000/process')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setResponseData(data);
        setSuccess(true);
      })
      .catch(error => {
        console.error('Fetch error:', error);
        setError(true);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        {loading && <p>Please wait while handling backend API call</p>}
        {loading && <img src={spinner} className="App-logo" alt="spinner" />}

        {!loading && success && <p>✅ Backend call succeeded</p>}
        {!loading && error && <p style={{ color: 'red' }}>❌ Service error, please contact support.</p>}

        {/* Show response JSON data */}
        {!loading && responseData && (
          <pre style={{ textAlign: 'left', backgroundColor: '#transparent', padding: '1em', borderRadius: '8px' }}>
            {JSON.stringify(responseData, null, 2)}
          </pre>
        )}
      </header>
    </div>
  );
}

export default App;
