import React, {useEffect, useState} from 'react';
import './App.css';
import Login from './components/Login'
import Home from './components/Home';
import axios from "axios";

const baseUrl = "http://localhost:5000";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(true);
    
  const checkSession = async () => {
    try {
      const response = await axios.post(`${baseUrl}/auth/check_session`, {
        id: localStorage.getItem('id'),
        access_token: localStorage.getItem('access_token'),
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      const sessionActive = response.data.session_active;

      if (!sessionActive) {
        logout(); // Automatically logout if the session is not active
      }

      setIsLoggedIn(sessionActive);
    } catch (error) {
      console.log(`Error fetching data from the server: `, error);
      setIsLoggedIn(false);
    }
  }
  
  useEffect(() => {
    checkSession();
  }, [checkSession]);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const logout = () => {
    axios.post(
        `${baseUrl}/auth/logout`,
        JSON.stringify({ "id": localStorage.getItem('id') }),
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
    )
        .then(response => {
          if (response.status === 200) {
            console.log('User logged out successfully');
            localStorage.removeItem('access_token');
            setIsLoggedIn(false);
            console.log('LOGGED OUT');
          } else {
            console.log('User logout failed');
          }
        })
        .catch(error => {
          console.log(`Error fetching data from the server: `, error);
        });
  };

  const handleLogout = (e) => {
    logout();
    e.preventDefault();
  };

  return (
    <div className="App">

      <header>
        <div class="header-left">
          <h1>NutriKit</h1>
        </div>
        <div class="header-right">
          <nav>
            <ul>
              { isLoggedIn && (
                <li>
                  <button className="nav-link" onClick={handleLogout}>Logout</button>
                </li>
              )}
            </ul>
          </nav>
        </div>
      </header>

      {isLoggedIn ? <Home /> : <Login handleLogin={handleLogin} />}

      <footer>
        <p>Group-3</p>
      </footer>

      
    </div>
    
  );
}

export default App;