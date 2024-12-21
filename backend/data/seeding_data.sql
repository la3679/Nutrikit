



INSERT INTO users (id,display_name,email,password_hash,height,weight) 
VALUES('person1','person1','person1@rit.edu','3c9909afec25354d551dae21590bb26e3
	   8d53f2173b8d3dc3eee4c047e7ab1c1eb8b85103e3be7ba613b31bb5c9c36214dc
	   9f14a42fd7a2fdb84856bca5c44c2',183,80);


INSERT INTO diet_goals(user_id,start_date,end_date,active,protein,fats,carbs) 
VALUES ('person1',CURRENT_DATE,CURRENT_DATE+30,TRUE,160,80,250);


INSERT INTO items(item_name,item_type,item_category) 
VALUES ('Banana','food_item','fruit'),
('Egg','food_item','diary'),
('Sandwich','meal',NULL),
('Tomato','food_item','vegetables');


INSERT INTO meal_components(item_id,food_item_id,quantity) 
VALUES (3,4,1),
(3,2,1);


INSERT INTO diet_trackers(user_id,item_id,consumed_time,amount)
VALUES ('person1',1,CURRENT_TIMESTAMP,1),
('person1',2,CURRENT_TIMESTAMP,1),
('person1',3,CURRENT_TIMESTAMP,1);