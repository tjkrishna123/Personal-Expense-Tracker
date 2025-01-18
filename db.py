## Necessary packages Installation
#!pip install faker
#!pip install mysql-connector-python



#Importing necessary libraries for creating a fake database in mySQL

import random
import pandas as pd
import mysql.connector
from faker import Faker
from datetime import date


#Intitialising faker()

fake = Faker()

#Creating a list of categories and payment_modes.

categories = ['Grocery','Fruits','Vegetables','Medicine','Petrol','E-commerce','Food delivery','Rent','School fee','Investment','EMI','Property tax','Transportation','Gifts','Accomodation','Insurance premium','Subscription','Bills']
payment_modes = ['Cash','UPI','Credit card','Debit card','Net banking','Mobile banking']


#Function defination for creating monthly_expense data
def monthly_expense(entries,start_date,end_date):

  data =[] #Initialise list for data append
  for i in range(entries):
    category = random.choice(categories)  # Choose category first

    # Define amount ranges for each category (example values)
    if category == 'Rent':
      amount = round(random.uniform(15000, 20000))
    elif category == 'Investment':
      amount = round(random.uniform(10000, 20000))
    elif category == 'EMI':
      amount = round(random.uniform(7000, 9000))
    elif category == 'Insurance premium':
      amount = round(random.uniform(1000, 2000))
    elif category == 'School fee':
      amount = round(random.uniform(5000, 9000))
    
    else:  # Default range if category not specified above
      amount = round(random.uniform(40, 500))

    # Geneating fake data in dictionary   
    expense_data = {
          'Date' : fake.date_between_dates(date_start=start_date,date_end=end_date),
          'Category' : category,
          'Payment_mode' : random.choice(payment_modes),
          'Amount' : amount,
          'Description' : fake.sentence(),
          'Cashback' : round(random.uniform(0,25)),
    }
    data.append(expense_data) #Appending expense_data to list data
  return pd.DataFrame(data) # Function returns "data" in the form of dataframe 

#Function call for Each month
Jan = monthly_expense(150,date(2024,1,1),date(2024,1,31))
Feb = monthly_expense(200,date(2024,2,1),date(2024,2,29))
Mar = monthly_expense(150,date(2024,3,1),date(2024,3,31))
Apr = monthly_expense(200,date(2024,4,1),date(2024,4,30))
May = monthly_expense(150,date(2024,5,1),date(2024,5,31))
Jun = monthly_expense(200,date(2024,6,1),date(2024,6,30))
Jul = monthly_expense(150,date(2024,7,1),date(2024,7,31))
Aug = monthly_expense(200,date(2024,8,1),date(2024,8,31))
Sep = monthly_expense(150,date(2024,9,1),date(2024,9,30))
Oct = monthly_expense(200,date(2024,10,1),date(2024,10,31))
Nov = monthly_expense(150,date(2024,11,1),date(2024,11,30))
Dec = monthly_expense(200,date(2024,12,1),date(2024,12,31))


#Concatinating all 12 months data in yearly_exp_data
yearly_exp_data = pd.concat([Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec])

#Creating connection with mySQL
mycon = mysql.connector.connect(
    host ="localhost",
    user = "root",
    password = "12345",
    database = "expense_tracker"

)

#Creating cursor to execute queries.
mycursor = mycon.cursor(dictionary=True)

#Query for creating Table
create_table_query = "create table exp (Date date, Category varchar(50), Payment_mode varchar(30), Amount int, Description varchar(200), Cashback int ) "
mycursor.execute(create_table_query)

#Query for inserting table
insert_query = "insert into exp values(%s,%s,%s,%s,%s,%s)"
data_list = [tuple(row.astype(str)) for _, row in yearly_exp_data.iterrows()]
mycursor.executemany(insert_query, data_list)
mycon.commit()