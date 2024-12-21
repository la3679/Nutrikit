DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS items CASCADE;
DROP TABLE IF EXISTS item_tags CASCADE;
DROP TABLE IF EXISTS meal_components CASCADE;
DROP TABLE IF EXISTS nutrition_info CASCADE;
DROP TABLE IF EXISTS diet_goals CASCADE;
DROP TABLE IF EXISTS diet_plans CASCADE;
DROP TABLE IF EXISTS diet_trackers CASCADE;

CREATE TABLE users (
    id VARCHAR(50) PRIMARY KEY NOT NULL,
    display_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    height FLOAT,
    weight FLOAT,
    session_key VARCHAR(128) DEFAULT NULL
);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    item_type VARCHAR(20) NOT NULL,
    item_category VARCHAR(20) NOT NULL
);

CREATE TABLE item_tags (
    id SERIAL PRIMARY KEY,
    item_id INT NOT NULL,
    tag VARCHAR(255) NOT NULL,
    FOREIGN KEY (item_id) REFERENCES items (id)
);

CREATE TABLE meal_components (
    id SERIAL PRIMARY KEY,
    item_id INT NOT NULL,
    meal_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (item_id) REFERENCES items (id)
);

CREATE TABLE nutrition_info (
    id SERIAL PRIMARY KEY,
    item_id INT NOT NULL,
    unit VARCHAR(255) NOT NULL,
    protein FLOAT DEFAULT 0,
    carbs FLOAT DEFAULT 0,
    fats FLOAT DEFAULT 0,
    FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE
);

CREATE TABLE diet_goals (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    active BOOLEAN NOT NULL,
    protein INT DEFAULT 0,
    fats INT DEFAULT 0,
    carbs INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE diet_plans (
    id SERIAL PRIMARY KEY,
    diet_goal_id INT NOT NULL,
    item_id INT NOT NULL,
    time_to_consume TIMESTAMP NOT NULL,
    amount FLOAT NOT NULL,
    FOREIGN KEY (diet_goal_id) REFERENCES diet_goals (id),
    FOREIGN KEY (item_id) REFERENCES items (id)
);

CREATE TABLE diet_trackers (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    item_id INT NOT NULL,
    consumed_time TIMESTAMP NOT NULL,
    amount INT NOT NULL,
    FOREIGN KEY (item_id) REFERENCES items (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);
