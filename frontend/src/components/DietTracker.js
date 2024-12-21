import React, {useEffect, useState, useCallback} from 'react';
import '../App.css';
import axios from "axios";

const baseUrl = 'http://localhost:5000';

function DietTracker() {
    const [foodData, setFoodData] = useState([]);
    const [trackingData, setTrackingData] = useState([]);
    const [dailyFats, setDailyFats] = useState(0);
    const [dailyCarbs, setDailyCarbs] = useState(0);
    const [dailyProtein, setDailyProtein] = useState(0);
    const [selectedFood, setSelectedFood] = useState(null);
    const [quantity, setQuantity] = useState(1);

    const loadTrackedItems = useCallback(() => {
        axios.get(`${baseUrl}/tracker`, {
            headers: {
                'Content-Type': 'application/json',
                'userid': localStorage.getItem('id')
            }
        })
            .then(response => {
                if (response.status === 200) {
                    setTrackingData(response.data)
                    let totalProtein = 0;
                    let totalCarbs = 0;
                    let totalFats = 0;
                    response.data.forEach(item => {
                        totalProtein += item['protein'] * item['amount'];
                        totalCarbs += item['carbs'] * item['amount'];
                        totalFats += item['fats'] * item['amount'];
                    });
                    setDailyProtein(totalProtein);
                    setDailyCarbs(totalCarbs);
                    setDailyFats(totalFats);
                } else {
                    console.log('Get Diet tracking data failed..');
                }
            })
            .catch(error => {
                console.log(`Error fetching data from the server: `, error);
            });

    }, []);

    const loadFoodData = useCallback(() => {
        const storedFoodData = localStorage.getItem('foodData');

        if (storedFoodData) {
            setFoodData(JSON.parse(storedFoodData));
        } else {
            axios.get(`${baseUrl}/items`, {
                headers: {
                    'Content-Type': 'application/json'
                }
            })
                .then(response => {
                    if (response.status === 200) {
                        const data = response.data;
                        setFoodData(data);
                        localStorage.setItem('foodData', JSON.stringify(data));
                    } else {
                        console.log('Get Food items failed.');
                    }
                })
                .catch(error => {
                    console.log(`Error fetching data from the server: `, error);
                });
        }

        loadTrackedItems();
    } , [loadTrackedItems]);


    useEffect(() => {
        loadFoodData();
        loadTrackedItems();
    }, [loadFoodData, loadTrackedItems]);

    const handleAddFoodItem = async (item, amount) => {
        if (selectedFood && quantity) {
            try {
                await axios.post(
                    `${baseUrl}/tracker`,
                    JSON.stringify({
                        user_id: localStorage.getItem('id'),
                        item_id: item.id,
                        amount: amount
                    }),
                    {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }
                );
    
                console.log('Intake log added..');
            } catch (error) {
                console.log('Post Diet tracking failed..', error);
            }
    
            loadTrackedItems();
        }
    };

    const deleteTrackedItem = async (id) => {
        try {
            await axios.delete(`${baseUrl}/tracker`, {
                headers: {
                    'Content-Type': 'application/json'
                },
                params: {
                    user_id: localStorage.getItem('id'),
                    entry_id: id
                }
            });
    
            console.log('Intake log deleted..');
        } catch (error) {
            console.log('Delete Diet tracking failed..', error);
        }
    
        loadTrackedItems();
    };

        return (
        <div className="Tracker">
            <h1>My Diet Tracker</h1>
            <h3>Daily Intake</h3>
            <p>Protein: {dailyProtein} g</p>
            <p>Fats: {dailyFats} g</p>
            <p>Carbs: {dailyCarbs} g</p>
            <select onChange={(e) => setSelectedFood(foodData[e.target.value])}>
                <option value="" disabled selected>Select food items</option>
                {foodData.map((item, index) => (
                    <option key={index} value={index}>
                        {item.item_name} (Carbs: {item.carbs} g, Fats: {item.fats} g, Protein: {item.protein} g)
                    </option>
                ))}
            </select>
            <input
                type="number"
                min="1"
                value={quantity}
                onChange={(e) => setQuantity(e.target.value)}
            />
            <button onClick={() => handleAddFoodItem(selectedFood, quantity)}>Add Food Item</button>
            <br/>
            <table>
                <thead>
                <tr>
                    <th>Item Name</th>
                    <th>Consumption Time</th>
                    <th>Quantity</th>
                    <th>Item Category</th>
                    <th>Action</th>
                </tr>
                </thead>
                <tbody>
                {trackingData.map((item, index) => (
                    <tr className="food-item" key={index}>
                        <td>{item.item_name}</td>
                        <td>{item.consumed_time}</td>
                        <td>{item.amount}</td>
                        <td>{item.item_category}</td>
                        <td><button onClick={() => deleteTrackedItem(item.entry_id)}>Delete</button></td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
}
export default DietTracker;