import React, { useEffect, useState, useCallback } from 'react';
import '../App.css';
import axios from "axios";

const baseUrl = 'http://localhost:5000';

function DietGoals() {
    const [dietGoals, setDietGoals] = useState([]);
    const [formData, setFormData] = useState({
        start_date: '',
        end_date: '',
        protein: '',
        fats: '',
        carbs: ''
    });
    
    const loadData = () => {
        axios.get(`${baseUrl}/diet/all`, {
            headers: {
                'Content-Type': 'application/json',
                'userid': localStorage.getItem('id')
            }
        })
            .then(response => {
                if (response.status === 200) {
                    const data = response.data;
                    setDietGoals(data);
                } else {
                    console.log('Get Food items failed.');
                }
            })
            .catch(error => {
                console.log(`Error fetching data from the server: `, error);
            });
    }

    const makeActive = useCallback(async (id) => {
        try {
            await axios.put(
                `${baseUrl}/diet`,
                JSON.stringify({
                    user_id: localStorage.getItem('id'),
                    id: id,
                    active: true
                }),
                {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }
            );

            console.log('Active DietGoal updated..');
            loadData();
        } catch (error) {
            console.log('Post Diet tracking failed..', error);
        }
    }, []); 

    const deleteDietGoal = useCallback(async (id) => {
        try {
            await axios.delete(`${baseUrl}/diet`, {
                headers: {
                    'Content-Type': 'application/json'
                },
                params: {
                    id: id
                }
            });

            console.log('Diet Goal deleted..');
            loadData();
        } catch (error) {
            console.log('Delete Diet Goal failed..', error);
        }
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        let request_body = {...formData}
        request_body['user_id'] = localStorage.getItem('id');
        let in_date = request_body.start_date.split('-');
        request_body['start_date'] = in_date[1] + '/' + in_date[2] + '/' + in_date[0];
        in_date = request_body.end_date.split('-');
        request_body['end_date'] = in_date[1] + '/' + in_date[2] + '/' + in_date[0];
        try {
            await axios.post(`${baseUrl}/diet`, request_body, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            console.log('Diet Goal added..');
            loadData();
        } catch (error) {
            console.log('Post Diet Goal failed..', error);
        }
    };

    const handleInputChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    useEffect(() => {
        loadData();
    }, []);

    return (
        <div className="DietGoals">
            <h1>My Diet Goals</h1>
            <br></br>
            

            <form onSubmit={handleSubmit} class="login-form">
                <div class="form-group">
                    <label>Start Date: </label>
                    <input type="date" name="start_date" value={formData.start_date} onChange={handleInputChange} required />
                </div>
                <div class="form-group">
                    <label>End Date: </label>
                    <input type="date" name="end_date" value={formData.end_date} onChange={handleInputChange} required />
                </div>
                <div class="form-group">
                    <label>Protein: </label>
                    <input type="number" name="protein" value={formData.protein} onChange={handleInputChange} required />
                </div>
                <div class="form-group">
                    <label>Fats: </label>
                    <input type="number" name="fats" value={formData.fats} onChange={handleInputChange} required />
                </div>
                <div class="form-group">
                    <label>Carbs: </label>
                    <input type="number" name="carbs" value={formData.carbs} onChange={handleInputChange} required />
                </div>
                <button type="submit" >Add Diet Goal</button>
            </form>
            <br></br>
            <table>
                <thead>
                    <tr>
                        <th>Active</th>
                        <th>Start Date</th>
                        <th>End Date</th>
                        <th>Protein</th>
                        <th>Fats</th>
                        <th>Carbs</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {dietGoals.map((item, index) => (
                        <tr className="diet-goals" key={index}>
                            <td>
                                <center><input
                                    type="radio"
                                    name={item.id}
                                    checked={item.active}
                                    onChange={() => makeActive(item.id)}
                                /></center>
                            </td>
                            <td>{item.start_date}</td>
                            <td>{item.end_date}</td>
                            <td>{item.protein}</td>
                            <td>{item.fats}</td>
                            <td>{item.carbs}</td>
                            <td><button onClick={() => deleteDietGoal(item.id)}>Delete</button></td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
export default DietGoals;