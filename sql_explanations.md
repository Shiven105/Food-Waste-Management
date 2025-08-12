# SQL Explanations for the 15 queries

1) Providers & Receivers per city
   - Purpose: Count how many providers and receivers exist in each city.
   - Main idea: Use a UNION of cities from both tables to iterate through all cities, then use subqueries to count providers and receivers matching each city.

2) Top provider types by listings
   - Purpose: Find which provider types (Restaurant, Grocery, etc.) have the most food listings.
   - Main idea: Group listings by Provider_Type and count rows; order descending.

3) Contacts of providers (sample)
   - Purpose: Provide contact information for providers for coordination.
   - Main idea: Select Name, Address, City, Contact from providers. Limit for display.

4) Receivers with most claims
   - Purpose: Identify receivers who claim most often (could indicate recurring NGOs).
   - Main idea: Left join receivers to claims and group by receiver, count claims.

5) Total quantity available
   - Purpose: Sum of quantities across all current food listings.
   - Main idea: Use SUM(Quantity) on the food_listings table.

6) City with highest listings
   - Purpose: Find cities that host the most food listings (hotspots).
   - Main idea: Group by Location and count; order and limit top 10.

7) Most common food types
   - Purpose: Which categories of food are most frequently available?
   - Main idea: Group by Food_Type and count.

8) Claims per food item
   - Purpose: How many times each food item has been claimed.
   - Main idea: Left join claims to food_listings and count claims per Food_ID.

9) Provider with most successful claims
   - Purpose: Which providers had the most completed claims (i.e., successful distributions).
   - Main idea: Join providers->food_listings->claims and filter Status='completed', group by provider.

10) Claims status percentage
    - Purpose: Show distribution of claim statuses (Pending/Completed/Cancelled) as counts and percentages.
    - Main idea: Group claims by Status and compute percentage of total claims.

11) Average quantity claimed per receiver
    - Purpose: Average quantity available for the items claimed by each receiver (proxy for average claim size).
    - Main idea: Join receivers->claims->food_listings and average the quantities.

12) Most claimed meal type
    - Purpose: Find which meal types (Breakfast/Lunch/Dinner/Snacks) are most claimed.
    - Main idea: Join claims to food_listings and group by Meal_Type.

13) Total quantity donated by each provider
    - Purpose: Sum donated quantities per provider to see top donors.
    - Main idea: Left join providers to food_listings and SUM quantities, group by provider.

14) Top food items by quantity
    - Purpose: Which specific food items have the highest total quantities?
    - Main idea: Group by Food_Name and SUM Quantity, order desc.

15) Expiring soon items
    - Purpose: List items with closest expiry dates to prioritize redistribution.
    - Main idea: Order food_listings by Expiry_Date ascending and limit.