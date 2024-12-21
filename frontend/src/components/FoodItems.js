import React, { useState, useEffect } from 'react';
import axios from 'axios';

const baseUrl = 'http://localhost:5000';

const FoodItems = (props) => {
  const [selectedFood, setSelectedFood] = useState(null);
  const [foodData, setFoodData] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);

  useEffect(() => {
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
  }, []);

  const handleClick = (food) => {
    setSelectedFood(food);
  };

  const handleClose = () => {
    setSelectedFood(null);
  };

  const handleCategoryChange = (event) => {
    setSelectedCategory(event.target.value);
  };

  const filteredFoodData = selectedCategory
    ? foodData.filter(food => food.item_category === selectedCategory)
    : foodData;

  return (
    <div className="Items">
      <div>
        <label htmlFor="category">Select Category: </label>
        <select id="category" onChange={handleCategoryChange}>
          <option value="">All Categories</option>
          {Array.from(new Set(foodData.map(food => food.item_category))).map((item_category, index) => (
            <option key={index} value={item_category}>{item_category}</option>
          ))}
        </select>
      </div>

      <br></br>

      {filteredFoodData.map((food, index) => (
        <div className="food-item" key={index} onClick={() => handleClick(food)}>
          {food.item_name}
        </div>
      ))}

      {selectedFood && (
        <div className="modal">
          <h2>{selectedFood.item_name}</h2>
          <br></br>
          <p>Carbs: {selectedFood.carbs} grams</p>
          <p>Proteins: {selectedFood.proteins} grams</p>
          <p>Fats: {selectedFood.fats} grams</p>
          <p>Category: {selectedFood.item_category}</p>
          <button onClick={handleClose}>Close</button>
        </div>
      )}
    </div>
  );
}

export default FoodItems;