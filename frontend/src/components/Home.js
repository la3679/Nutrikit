import React,{useState} from 'react';
import '../App.css';
import FoodItems from './FoodItems';
import DietTracker from './DietTracker';
import DietGoals from "./DietGoals";

function Home(props) {
  const [username] = useState(localStorage.getItem('id'));
  const [selectedTab, setSelectedTab] = useState(localStorage.getItem('tab') || 'FoodItems');

  const handleTabChange = (tab) => {
      setSelectedTab(tab);
    };

    const renderTabContent = () => {
      switch (selectedTab) {
        case 'FoodItems':
          localStorage.setItem('tab', 'FoodItems');
          return <FoodItems/>;
        case 'DietTracker':
          localStorage.setItem('tab', 'DietTracker');
          return <DietTracker/>;
        case 'DietGoals':
          localStorage.setItem('tab', 'DietGoals');
          return <DietGoals />;
        // case 'tab4':
        //   return <Tab4Content />;
        default:
          return null;
      }
    };

  const buttons = document.querySelectorAll("Home-nav button");
  buttons.forEach((button) => {
    button.addEventListener("click", (event) => {
      const clickedButton = event.target;
      buttons.forEach((button) => {
        if (button !== clickedButton) {
          button.classList.remove("active");
        }
      });
      clickedButton.classList.add("active");
    });
  });

  return (
    <div className="App">
      <br></br>
      <h2 className='User-head'>
        Logged User: {username}
      </h2>
      <br></br>
      <nav className='Home-nav'>
      <button type="button" onClick={() => handleTabChange('FoodItems')} className={selectedTab === 'FoodItems' ? 'active' : ''}>
        Food/Meal Items
      </button>
      <button type="button" onClick={() => handleTabChange('DietTracker')} className={selectedTab === 'DietTracker' ? 'active' : ''}>
        Diet Tracker
      </button>
      <button type="button" onClick={() => handleTabChange('DietGoals')} className={selectedTab === 'DietGoals' ? 'active' : ''}>
        Diet Goals
      </button>
      <button type="button" onClick={() => handleTabChange('DietPlanner')} className={selectedTab === 'DietPlanner' ? 'active' : ''}>
        Diet Planner
      </button>

        {/* <button type="button" onClick={() => handleTabChange('FoodItems')}>
          Food/Meal Items
        </button>
        <button type="button" onClick={() => handleTabChange('DietTracker')}>
          Diet Tracker
        </button>
        <button type="button" onClick={() => handleTabChange('DietGoals')}>
          Diet Goals
        </button>
        <button type="button" onClick={() => handleTabChange('DietPlanner')}>
          Diet Planner
        </button> */}
      </nav>
      <main>
    <div className="tab-content" style={{ overflow: 'auto', height: 'calc(100vh - 35ex)' }}>
      {renderTabContent()}
    </div>
  </main>
    </div>
  );
}
export default Home;