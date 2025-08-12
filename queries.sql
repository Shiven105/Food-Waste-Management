-- 15 project queries
SELECT City, (SELECT COUNT(*) FROM providers p WHERE p.City = c.City) AS provider_count, (SELECT COUNT(*) FROM receivers r WHERE r.City = c.City) AS receiver_count FROM (SELECT City FROM providers UNION SELECT City FROM receivers) c GROUP BY City;
SELECT Provider_Type AS provider_type, COUNT(*) AS listings_count FROM food_listings GROUP BY Provider_Type ORDER BY listings_count DESC;
SELECT Name, Address, City, Contact, Type FROM providers LIMIT 200;
SELECT r.Receiver_ID, r.Name, COUNT(c.Claim_ID) AS claims_made FROM receivers r LEFT JOIN claims c ON r.Receiver_ID = c.Receiver_ID GROUP BY r.Receiver_ID, r.Name ORDER BY claims_made DESC;
SELECT SUM(Quantity) AS total_quantity_available FROM food_listings;
SELECT Location AS City, COUNT(*) AS listings_count FROM food_listings GROUP BY Location ORDER BY listings_count DESC LIMIT 10;
SELECT Food_Type, COUNT(*) AS count FROM food_listings GROUP BY Food_Type ORDER BY count DESC;
SELECT f.Food_ID, f.Food_Name, COUNT(c.Claim_ID) AS claims_count FROM food_listings f LEFT JOIN claims c ON f.Food_ID = c.Food_ID GROUP BY f.Food_ID, f.Food_Name ORDER BY claims_count DESC;
SELECT p.Provider_ID, p.Name, COUNT(c.Claim_ID) AS successful_claims FROM providers p JOIN food_listings f ON p.Provider_ID = f.Provider_ID JOIN claims c ON f.Food_ID = c.Food_ID WHERE lower(c.Status)='completed' GROUP BY p.Provider_ID, p.Name ORDER BY successful_claims DESC;
SELECT Status, COUNT(*) AS count, ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM claims),2) AS percentage FROM claims GROUP BY Status;
SELECT r.Receiver_ID, r.Name, AVG(IFNULL(f.Quantity,0)) AS avg_quantity FROM receivers r LEFT JOIN claims c ON r.Receiver_ID = c.Receiver_ID LEFT JOIN food_listings f ON c.Food_ID = f.Food_ID GROUP BY r.Receiver_ID, r.Name ORDER BY avg_quantity DESC;
SELECT Meal_Type, COUNT(c.Claim_ID) AS claims_count FROM claims c JOIN food_listings f ON c.Food_ID = f.Food_ID GROUP BY Meal_Type ORDER BY claims_count DESC;
SELECT p.Provider_ID, p.Name, SUM(f.Quantity) AS total_donated_quantity FROM providers p LEFT JOIN food_listings f ON p.Provider_ID = f.Provider_ID GROUP BY p.Provider_ID, p.Name ORDER BY total_donated_quantity DESC;
SELECT Food_Name, SUM(Quantity) AS total_quantity FROM food_listings GROUP BY Food_Name ORDER BY total_quantity DESC LIMIT 20;
SELECT Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Location FROM food_listings WHERE Expiry_Date IS NOT NULL ORDER BY Expiry_Date ASC LIMIT 50;