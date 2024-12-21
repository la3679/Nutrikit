import React, { useState } from 'react';
import '../App.css';
import axios from 'axios';

function Login(props) {
  const [isCreatingAccount, setCreatingAccount] = useState(false);
  const [id, setId] = useState('');
  const [password, setPassword] = useState('');

  const toggleForm = () => {
    setCreatingAccount(!isCreatingAccount);
  };

  const login = (id , password) => {
    console.log(id, password)
    let data= ({
      "id": id,
      "password": password
    })
    const baseUrl ='http://localhost:5000'
    axios.post(`${baseUrl}/auth/login`, JSON.stringify(data), {
      headers: {
        'Content-Type': 'application/json'
      }}, )
      .then(response => {
        if (response.status === 200) {
          console.log('User logged in successfully');
          localStorage.setItem('access_token', response.data.access_token);
          localStorage.setItem('id', id)
          console.log("LOGGED IN",response.data.access_token)
          props.handleLogin();
        } else if (response.status === 403) {
          console.log('User password incorrect');
        } else {
          console.log('User login failed');
        }
      })
      .catch(error => {
        console.log(`Error fetching data from the server: `, error);
      });
  }
  const handleLogin= (e) => {
    login(id, password);
    e.preventDefault();
  }

  return (
    <div className="App">      
      <main>
        <div className="login-form">
          <h2>{isCreatingAccount ? 'Create Account' : 'Login'}</h2>
          <form>
            {!isCreatingAccount && (
              <div>
                <div className="form-group">
                  <input type="id" placeholder="Enter your id" value={id} onChange={(e) => setId(e.target.value)} required/>
                </div>
                <div className="form-group">
                  <input type="password" placeholder="Enter your password" value={password} onChange={(e) => setPassword(e.target.value)} required/>
                </div>
                <button type="submit" onClick={handleLogin}>Login</button>
              </div>
            )}
            
            {isCreatingAccount && (
              <div>
                <div className="form-group">
                  <input type="text" placeholder="Enter your name" />
                </div>
                <div className="form-group">
                  <input type="text" placeholder="Enter your age" />
                </div>
                <div className="form-group">
                  <input type="text" placeholder="Enter your height" />
                </div>
                <div className="form-group">
                  <input type="text" placeholder="Enter your weight" />
                </div>
                <div className="form-group">
                  <input type="email" placeholder="Enter your email" />
                </div>
                <div className="form-group">
                  <input type="password" placeholder="Enter your password" />
                </div>
                <div className="form-group">
                  <input type="password" placeholder="Confirm your password" />
                </div>
                <button type="submit">Register</button>
              </div>
            )}
          </form>
          <p>
            {isCreatingAccount
              ? "Already have an account? "
              : "Don't have an account? "}
            <button onClick={toggleForm} className="link-button">
              {isCreatingAccount ? 'Login' : 'Create an account'}
            </button>
          </p>
        </div>
      </main>     
    </div>
  );
}

export default Login;
