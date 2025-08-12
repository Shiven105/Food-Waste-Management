
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
from streamlit_helpers import run_query, run_modify, get_table, to_csv_download_link

DB_PATH = "/mnt/data/food_waste.db"

st.set_page_config(page_title="Local Food Wastage Management System", layout="wide")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "EDA Dashboard", "Explore Listings", "Providers (CRUD)", "Food Listings (CRUD)", "Claims (CRUD)", "Queries & Reports", "Download Data"])

    if page == "Home":
        st.title("Local Food Wastage Management System")
        st.markdown("""
        **Purpose:** Connect surplus food providers with receivers to reduce local food waste.  
        **Features included:** Data exploration (EDA), filters, CRUD (Create/Read/Update/Delete) for providers, listings and claims, and 15+ SQL reports.
        """)
        st.info("Database: /mnt/data/food_waste.db (SQLite)")
        st.markdown("Use the sidebar to navigate.")

    elif page == "EDA Dashboard":
        st.header("Exploratory Data Analysis (EDA)")
        # KPIs
        q_total_providers = "SELECT COUNT(*) as cnt FROM providers"
        q_total_receivers = "SELECT COUNT(*) as cnt FROM receivers"
        q_total_listings = "SELECT COUNT(*) as cnt FROM food_listings"
        q_total_claims = "SELECT COUNT(*) as cnt FROM claims"
        cols = st.columns(4)
        try:
            cols[0].metric("Providers", int(run_query(q_total_providers).iloc[0,0]))
            cols[1].metric("Receivers", int(run_query(q_total_receivers).iloc[0,0]))
            cols[2].metric("Food Listings", int(run_query(q_total_listings).iloc[0,0]))
            cols[3].metric("Claims", int(run_query(q_total_claims).iloc[0,0]))
        except Exception as e:
            st.error("Error fetching KPIs: " + str(e))

        st.subheader("Top 10 Cities by Food Listings")
        df_cities = run_query("SELECT Location as City, COUNT(*) as listings FROM food_listings GROUP BY Location ORDER BY listings DESC LIMIT 10")
        st.bar_chart(df_cities.set_index("City"))

        st.subheader("Most Common Food Types")
        df_foodtypes = run_query("SELECT Food_Type, COUNT(*) as cnt FROM food_listings GROUP BY Food_Type ORDER BY cnt DESC")
        st.table(df_foodtypes)

        st.subheader("Expiring Soon (next 30 days)")
        df_exp = run_query("SELECT Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Location FROM food_listings WHERE Expiry_Date IS NOT NULL ORDER BY Expiry_Date ASC LIMIT 50")
        st.dataframe(df_exp)

    elif page == "Explore Listings":
        st.header("Explore / Filter Food Listings")
        df = run_query("SELECT f.*, p.Name as Provider_Name FROM food_listings f LEFT JOIN providers p ON f.Provider_ID = p.Provider_ID")
        city = st.selectbox("City", options=["All"] + sorted(df['Location'].dropna().unique().tolist()))
        ftype = st.selectbox("Food Type", options=["All"] + sorted(df['Food_Type'].dropna().unique().tolist()))
        meal = st.selectbox("Meal Type", options=["All"] + sorted(df['Meal_Type'].dropna().unique().tolist()))
        provider = st.selectbox("Provider", options=["All"] + sorted(df['Provider_Name'].dropna().unique().tolist()))
        filtered = df.copy()
        if city != "All":
            filtered = filtered[filtered['Location'] == city]
        if ftype != "All":
            filtered = filtered[filtered['Food_Type'] == ftype]
        if meal != "All":
            filtered = filtered[filtered['Meal_Type'] == meal]
        if provider != "All":
            filtered = filtered[filtered['Provider_Name'] == provider]
        st.write(f"Showing {len(filtered)} rows")
        st.dataframe(filtered)

    elif page == "Providers (CRUD)":
        st.header("Providers - View / Add / Edit / Delete")
        df = run_query("SELECT * FROM providers")
        st.dataframe(df)
        with st.expander("Add new provider"):
            name = st.text_input("Name")
            ptype = st.text_input("Type")
            address = st.text_input("Address")
            city = st.text_input("City")
            contact = st.text_input("Contact")
            if st.button("Add provider"):
                run_modify("INSERT INTO providers (Name, Type, Address, City, Contact) VALUES (?,?,?,?,?)", (name, ptype, address, city, contact))
                st.success("Provider added. Refresh the page to see changes.")

        with st.expander("Edit provider"):
            sel = st.selectbox("Select provider to edit", options=df['Provider_ID'].dropna().astype(str).tolist())
            if sel:
                row = df[df['Provider_ID']==int(sel)].iloc[0]
                name = st.text_input("Name", row['Name'])
                ptype = st.text_input("Type", row['Type'])
                address = st.text_input("Address", row['Address'])
                city = st.text_input("City", row['City'])
                contact = st.text_input("Contact", row['Contact'])
                if st.button("Save changes"):
                    run_modify("UPDATE providers SET Name=?, Type=?, Address=?, City=?, Contact=? WHERE Provider_ID=?", (name, ptype, address, city, contact, int(sel)))
                    st.success("Provider updated. Refresh page to see changes.")

        with st.expander("Delete provider"):
            sel = st.selectbox("Select provider to delete", options=[""] + df['Provider_ID'].dropna().astype(str).tolist())
            if sel and st.button("Delete provider"):
                run_modify("DELETE FROM providers WHERE Provider_ID=?", (int(sel),))
                st.success("Provider deleted (if constraints allow). Refresh page.")

    elif page == "Food Listings (CRUD)":
        st.header("Food Listings - View / Add /Edit / Delete")
        df = run_query("SELECT * FROM food_listings")
        st.dataframe(df)
        with st.expander("Add new listing"):
            fname = st.text_input("Food Name")
            qty = st.number_input("Quantity", min_value=0, value=1)
            exp = st.date_input("Expiry Date (leave as today if unknown)")
            pid = st.number_input("Provider_ID", min_value=0, value=1)
            ptype = st.text_input("Provider Type")
            location = st.text_input("Location/City")
            ftype = st.text_input("Food Type (e.g. Vegetarian)")
            meal = st.text_input("Meal Type (Breakfast/Lunch/Dinner/Snacks)")
            if st.button("Add listing"):
                exp_str = exp.strftime("%Y-%m-%d") if exp else None
                run_modify("INSERT INTO food_listings (Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type) VALUES (?,?,?,?,?,?,?,?)",
                           (fname, int(qty), exp_str, int(pid), ptype, location, ftype, meal))
                st.success("Listing added. Refresh page to see changes.")

        with st.expander("Edit listing"):
            sel = st.selectbox("Select Food_ID to edit", options=df['Food_ID'].dropna().astype(str).tolist())
            if sel:
                row = df[df['Food_ID']==int(sel)].iloc[0]
                fname = st.text_input("Food Name", row['Food_Name'])
                qty = st.number_input("Quantity", min_value=0, value=int(row['Quantity'] if pd.notnull(row['Quantity']) else 1))
                exp = st.date_input("Expiry Date", value=(pd.to_datetime(row['Expiry_Date']).date() if pd.notnull(row['Expiry_Date']) else datetime.today().date()))
                pid = st.number_input("Provider_ID", min_value=0, value=int(row['Provider_ID'] if pd.notnull(row['Provider_ID']) else 1))
                ptype = st.text_input("Provider Type", row['Provider_Type'])
                location = st.text_input("Location/City", row['Location'])
                ftype = st.text_input("Food Type", row['Food_Type'])
                meal = st.text_input("Meal Type", row['Meal_Type'])
                if st.button("Save listing changes"):
                    exp_str = exp.strftime("%Y-%m-%d") if exp else None
                    run_modify("UPDATE food_listings SET Food_Name=?, Quantity=?, Expiry_Date=?, Provider_ID=?, Provider_Type=?, Location=?, Food_Type=?, Meal_Type=? WHERE Food_ID=?",
                               (fname, int(qty), exp_str, int(pid), ptype, location, ftype, meal, int(sel)))
                    st.success("Listing updated. Refresh page.")

        with st.expander("Delete listing"):
            sel = st.selectbox("Select Food_ID to delete", options=[""] + df['Food_ID'].dropna().astype(str).tolist())
            if sel and st.button("Delete listing"):
                run_modify("DELETE FROM food_listings WHERE Food_ID=?", (int(sel),))
                st.success("Listing deleted.")

    elif page == "Claims (CRUD)":
        st.header("Claims - View / Make / Update / Cancel")
        dfc = run_query("SELECT c.*, r.Name as Receiver_Name, f.Food_Name FROM claims c LEFT JOIN receivers r ON c.Receiver_ID = r.Receiver_ID LEFT JOIN food_listings f ON c.Food_ID = f.Food_ID")
        st.dataframe(dfc)
        with st.expander("Make a claim"):
            food_id = st.number_input("Food_ID", min_value=0, value=1)
            receiver_id = st.number_input("Receiver_ID", min_value=0, value=1)
            status = st.selectbox("Status", options=["Pending","Completed","Cancelled"])
            if st.button("Make claim"):
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                run_modify("INSERT INTO claims (Food_ID, Receiver_ID, Status, Timestamp) VALUES (?,?,?,?)", (int(food_id), int(receiver_id), status, ts))
                st.success("Claim created. Refresh page.")

        with st.expander("Update claim status"):
            sel = st.selectbox("Select Claim_ID", options=[""] + dfc['Claim_ID'].dropna().astype(str).tolist())
            if sel:
                new_status = st.selectbox("New status", options=["Pending","Completed","Cancelled"])
                if st.button("Update status"):
                    run_modify("UPDATE claims SET Status=? WHERE Claim_ID=?", (new_status, int(sel)))
                    st.success("Claim status updated.")

    elif page == "Queries & Reports":
        st.header("Prebuilt SQL Queries (15)")
        st.markdown("These queries answer the project questions. Select one to run and view results. You can also download CSV.")
        sqls = {
            "Providers & Receivers per city": "SELECT City, (SELECT COUNT(*) FROM providers p WHERE p.City = c.City) AS provider_count, (SELECT COUNT(*) FROM receivers r WHERE r.City = c.City) AS receiver_count FROM (SELECT City FROM providers UNION SELECT City FROM receivers) c GROUP BY City;",
            "Top provider types by listings": "SELECT Provider_Type AS provider_type, COUNT(*) AS listings_count FROM food_listings GROUP BY Provider_Type ORDER BY listings_count DESC;",
            "Contacts of providers (sample)": "SELECT Name, Address, City, Contact, Type FROM providers LIMIT 200;",
            "Receivers with most claims": "SELECT r.Receiver_ID, r.Name, COUNT(c.Claim_ID) AS claims_made FROM receivers r LEFT JOIN claims c ON r.Receiver_ID = c.Receiver_ID GROUP BY r.Receiver_ID, r.Name ORDER BY claims_made DESC;",
            "Total quantity available": "SELECT SUM(Quantity) AS total_quantity_available FROM food_listings;",
            "City with highest listings": "SELECT Location AS City, COUNT(*) AS listings_count FROM food_listings GROUP BY Location ORDER BY listings_count DESC LIMIT 10;",
            "Most common food types": "SELECT Food_Type, COUNT(*) AS count FROM food_listings GROUP BY Food_Type ORDER BY count DESC;",
            "Claims per food item": "SELECT f.Food_ID, f.Food_Name, COUNT(c.Claim_ID) AS claims_count FROM food_listings f LEFT JOIN claims c ON f.Food_ID = c.Food_ID GROUP BY f.Food_ID, f.Food_Name ORDER BY claims_count DESC;",
            "Provider with most successful claims": "SELECT p.Provider_ID, p.Name, COUNT(c.Claim_ID) AS successful_claims FROM providers p JOIN food_listings f ON p.Provider_ID = f.Provider_ID JOIN claims c ON f.Food_ID = c.Food_ID WHERE lower(c.Status)='completed' GROUP BY p.Provider_ID, p.Name ORDER BY successful_claims DESC;",
            "Claims status percentage": "SELECT Status, COUNT(*) AS count, ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM claims),2) AS percentage FROM claims GROUP BY Status;",
            "Average quantity of food per receiver (their claimed items' quantities)": "SELECT r.Receiver_ID, r.Name, AVG(IFNULL(f.Quantity,0)) AS avg_quantity FROM receivers r LEFT JOIN claims c ON r.Receiver_ID = c.Receiver_ID LEFT JOIN food_listings f ON c.Food_ID = f.Food_ID GROUP BY r.Receiver_ID, r.Name ORDER BY avg_quantity DESC;",
            "Most claimed meal type": "SELECT Meal_Type, COUNT(c.Claim_ID) AS claims_count FROM claims c JOIN food_listings f ON c.Food_ID = f.Food_ID GROUP BY Meal_Type ORDER BY claims_count DESC;",
            "Total quantity donated by each provider": "SELECT p.Provider_ID, p.Name, SUM(f.Quantity) AS total_donated_quantity FROM providers p LEFT JOIN food_listings f ON p.Provider_ID = f.Provider_ID GROUP BY p.Provider_ID, p.Name ORDER BY total_donated_quantity DESC;",
            "Top food items by quantity": "SELECT Food_Name, SUM(Quantity) AS total_quantity FROM food_listings GROUP BY Food_Name ORDER BY total_quantity DESC LIMIT 20;",
            "Expiring soon items": "SELECT Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Location FROM food_listings WHERE Expiry_Date IS NOT NULL ORDER BY Expiry_Date ASC LIMIT 50;"
        }
        choice = st.selectbox("Choose query", options=list(sqls.keys()))
        if st.button("Run query"):
            dfq = run_query(sqls[choice])
            st.write(f"Result rows: {len(dfq)}")
            st.dataframe(dfq)
            st.markdown(to_csv_download_link(dfq, filename="query_result.csv"), unsafe_allow_html=True)

    elif page == "Download Data":
        st.header("Download cleaned CSVs or full DB")
        st.markdown("Download the cleaned CSV files or the SQLite DB for submission.")
        files = {
            "Clean Providers": "/mnt/data/clean_providers.csv",
            "Clean Receivers": "/mnt/data/clean_receivers.csv",
            "Clean Food Listings": "/mnt/data/clean_food_listings.csv",
            "Clean Claims": "/mnt/data/clean_claims.csv",
            "SQLite DB": "/mnt/data/food_waste.db"
        }
        for label, path in files.items():
            try:
                with open(path, "rb") as f:
                    btn = st.download_button(label, f, file_name=path.split("/")[-1])
            except Exception as e:
                st.write("Error preparing", label, str(e))

if __name__ == "__main__":
    main()
