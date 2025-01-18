####******Installation of necessary libraries***####
#!pip install mysql-connector-python
#!apt-get -y install mysql-server


#Importing necessary libraries.
import mysql.connector
import pandas as pd
import streamlit as st
import plotly.express as px

#Creating connection
mycon = mysql.connector.connect(
    host ="localhost",
    user = "root",
    password = "12345",
    database = "expense_tracker"

)

#Creating cursor to execute query
mycursor = mycon.cursor(dictionary=True)

#Streamlit title for Navigation.
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Spendings", "Insights"])


#Execution of code and Query according to the user selection
if page == "Home":
    #Streamlit title and image for Home screen
    st.title("Welcome to the Expense Tracker Application")
    st.write("Use the sidebar to navigate to different sections.")
    st.image("expense-tracker-app.png", caption="Expense Tracker",use_column_width=True)

elif page=="Spendings":

    #Queries in dictionary
    queries = {
        "What is the total amount spent in each category?": "select category, sum(amount) as total from exp group by category order by total desc",
        "What is the total amount spent using each payment mode?": "select payment_mode,sum(amount) as total from exp group by payment_mode order by total desc",
        "What is the total cashback received across all transactions?": "select sum(cashback) as total from exp",
        "Which are the top 5 most expensive categories in terms of spending?": "select category, sum(amount) as total from exp group by category order by total DESC limit 5",
        "How much was spent on transportation using different payment modes?": "select payment_mode, sum(amount) as total from exp where category ='transportation' group by payment_mode",
        "Which transactions resulted in cashback?":"select * from exp where cashback > 0",
        "What is the total spending in each month of the year?":"SELECT  MONTHNAME(Date) AS Month, SUM(amount) AS Total_spending FROM exp GROUP BY  MONTH(Date),MONTHNAME(Date) ORDER BY MONTH(date)",
        "How much cashback or rewards were earned in each month?":"SELECT  MONTHNAME(Date) AS Month, SUM(Cashback) AS Total_Cashback FROM exp WHERE cashback > 0 GROUP BY  MONTH(Date),MONTHNAME(date) ORDER BY MONTH(date)",
        "What is the seasonal spending pattern across all seasons?":"SELECT CASE WHEN MONTH(Date) IN (12, 1, 2) THEN 'Winter'WHEN MONTH(Date) IN (3, 4, 5) THEN 'Spring'WHEN MONTH(Date) IN (6, 7, 8) THEN 'Summer'ELSE 'Fall'END AS Season,Category,SUM(amount) AS Total_Spending FROM exp GROUP BY Season, Category order by Total_Spending desc",
        "Total Spending and Cashback Summary?":"SELECT SUM(amount) AS Total_Spending, SUM(Cashback) AS Total_Cashback FROM exp;",
        "What is the count of different payment modes?": "SELECT payment_Mode, COUNT(*) AS Transaction_Count, SUM(amount) AS Total_Spending FROM exp GROUP BY payment_Mode",
        "Largest Transactions in Each Category?":"SELECT Category, MAX(amount) AS Largest_Transaction FROM exp GROUP BY Category;",
        "Which is the most frequently expensed category?":"SELECT Category, COUNT(*) AS Transaction_Count FROM exp GROUP BY Category ORDER BY Transaction_Count DESC",
        "What is the average spending per transaction?":"SELECT AVG(Amount) AS Average_Spending FROM exp;",
        "what is the average transaction amount in each month?": "SELECT MONTHNAME(Date) AS Month, AVG(amount) AS Average_Spending FROM exp GROUP BY  MONTH(Date), MONTHNAME(Date) ORDER BY MONTH(Date);",
        "Cashback percentage per transaction?":"SELECT Date, Category, amount, Cashback, (Cashback / amount) * 100 AS Cashback_Percentage FROM exp WHERE Cashback > 0 ORDER BY Cashback_Percentage DESC;",
        "what is the top 5 spending transaction?":"SELECT * FROM exp ORDER BY Amount DESC LIMIT 5;",
        "which cateogory of expenses gives highest cashback? and show me top 5?":"SELECT Category, SUM(Cashback) AS Total_Cashback FROM exp GROUP BY Category ORDER BY Total_Cashback DESC LIMIT 5;"
    }

    # Streamlit title for Spendings
    st.title("Analysis of Yearly spendings")
    st.subheader("Select any of the below options and  click RUN to know your spendings in detail.")

    # Query selection dropdown
    selected_query = st.selectbox("Choose a Query", list(queries.keys()))

    # Execute Query
    if st.button("RUN"):
        
        #Query execution and fetching data
        query = queries[selected_query]
        mycursor.execute(query)
        data = mycursor.fetchall()

        # Converting to dataframe
        df = pd.DataFrame(data)


        # Display result in table 
        st.table(df)

        #df['total']=df['total'].astype(float)
        #st.bar_chart(df,x="payment_mode", y="total", use_container_width=True)
        

        # Close connection
        mycursor.close()
        mycon.close()

elif page=="Insights":

    #Queries in dictionary
    queries = {
        "Total Spending accross different payment mode?": "select payment_mode,sum(amount) as total from exp group by payment_mode order by total desc",
        "Top 5 most expensive categories?": "select category, sum(amount) as total from exp group by category order by total DESC limit 5",
        "what is the monthly spending pattern?":"SELECT MONTH(Date) AS Month, SUM(Amount) AS Total_Spending FROM exp GROUP BY Month ORDER BY Month",
        "Total spending from each group in pie chart":"SELECT Category, SUM(Amount) AS Total_Spending FROM exp GROUP BY Category"
        
    }

    # Streamlit title for Spendings
    st.title("Insights of Yearly spendings")
    st.subheader("Select any of the below options and  click RUN for visual representation of spendings.")

    # Query selection dropdown
    selected_query = st.selectbox("Choose a Query", list(queries.keys()))

    # Execute Query
    if st.button("RUN"):
        
        if selected_query == "Total Spending accross different payment mode?":
            #Query execution and fetching data
            query = queries[selected_query]
            mycursor.execute(query)
            data = mycursor.fetchall()

            # Converting to dataframe
            df = pd.DataFrame(data)

            df['total']=df['total'].astype(float)
            st.bar_chart(df,x="payment_mode", y="total")
            

            # Close connection
            mycursor.close()
            mycon.close()

        elif selected_query == "Top 5 most expensive categories?":
            #Query execution and fetching data
            query = queries[selected_query]
            mycursor.execute(query)
            data = mycursor.fetchall()

            # Converting to dataframe
            df = pd.DataFrame(data)

            df['total']=df['total'].astype(float)
            st.bar_chart(df,x="category", y="total")
            

            # Close connection
            mycursor.close()
            mycon.close()

        elif selected_query == "what is the monthly spending pattern?":
            #Query execution and fetching data
            query = queries[selected_query]
            mycursor.execute(query)
            data = mycursor.fetchall()

            # Converting to dataframe
            df = pd.DataFrame(data)

            df['Total_Spending']=df['Total_Spending'].astype(float)
            st.line_chart(df, x="Month", y="Total_Spending", use_container_width=True)

            # Close connection
            mycursor.close()
            mycon.close()

        elif selected_query == "Total spending from each group in pie chart":
            #Query execution and fetching data
            query = queries[selected_query]
            mycursor.execute(query)
            data = mycursor.fetchall()

            # Converting to dataframe
            df = pd.DataFrame(data)

            df['Total_Spending']=df['Total_Spending'].astype(float)


          # Plot Pie Chart
            fig = px.pie(df, names="Category", values="Total_Spending", title="Spending by Category")
            st.plotly_chart(fig)

            # Close connection
            mycursor.close()
            mycon.close()
