# Packages

import pandas as pd
import datetime
import xlrd
import os
import sqlalchemy as db
import sqlite3
import matplotlib.pyplot as plt 

# SQL Connection

conn = sqlite3.connect('properties.sqlite')
cur=conn.cursor()

# Import Data

try:
    cur.execute('SELECT * FROM new_realinfo')
except:
    print("Table does not exist! Please wait as it is created...")
    df = pd.read_excel('Real_Est_Data_Final_Nov2019.xlsx')
    df.to_sql(name='new_realinfo', con=conn)

engine = db.create_engine('sqlite:///properties.sqlite', echo = True)
conn = engine.connect()

# Cleaning Data
cur.execute('CREATE TABLE IF NOT EXISTS new_realinfo AS SELECT * ORDER BY "YEAR"')
df = pd.read_sql_table('new_realinfo', conn)

df['Total_Assessed_Valuation'] = df['Assessed_Building_Value'] + df['Assessed_Land_Value']
df['Year'] = df['Total_Sale_Date'].dt.year
df = df[df["Land_classification"]=='R']
year = df.groupby(['Year'])
print(year['Total_Assessed_Valuation'].mean())

# Chart of initial data
y = year['Total_Sale_Date'].count()
z = year['Total_sale_Price'].mean()

y.plot()
plt.show()

z.plot()
plt.show()

# Function to analyze data by zipcode

input_yn = input('Would you like to view data by zipcode? (Y/N)').upper()

if input_yn == 'Y' or input_yn == 'YES':
    input_zip = int(input('Please enter the zipcode you would like to receive data for:'))
    filtered_data_zip_pre = df[df['PHYSICAL_ZIP_CODE']==input_zip]
    filtered_data_zip_pre = filtered_data_zip_pre.groupby('Year')
    filtered_data_zip = filtered_data_zip_pre['Total_sale_Price'].mean()
    filtered_data_zip.plot()
    z.plot()
    
    # zip_assess = input('Would you like to view home price vs. assessed home price? (Y/N) ').upper()
    # if zip_assess == 'Y' or zip_assess == 'YES':
    #     zip_assess_price = filtered_data_zip_pre['Total_Assessed_Valuation'].mean()
    #     print('Total Sale Price / Total Valuation Price: (Over 1 means the owner is paying above valuation, under 1 means the owner is paying below valuation.) ')
    #     zip_chart = filtered_data_zip_pre['Total_sale_Price'].mean() / zip_assess_price
    #     print(zip_chart)
    #     print('YOY Change is: ')
    #     print(zip_chart.pct_change(periods=2))
else:
    pass

# Function to analyze data by street

street_yn = input('Would you like to view data by street? (Y/N) ').upper()

if street_yn == 'Y' or street_yn == 'YES':
    prefix_yn = input('Is there a street prefix? (Y/N ) ').upper()
    if prefix_yn == 'Y' or prefix_yn == 'YES':
        input_prefix = input('Please enter the street prefix you would like to receive data for: (W, N, SE, etc.) ').upper()
        filtered_data_prefix = df[df["Street_Prefix"]==input_prefix]
    else:
        pass
    input_street = input('Please enter the street you would like to receive data for: ').upper()
    filtered_data_pre = df[df["Street_Name"]==input_street]
    filtered_data_pre = filtered_data_pre.groupby('Year')
    filtered_data = filtered_data_pre['Total_sale_Price'].mean()
    filtered_data.plot()
    z.plot()
    

else:
    pass

# Function to analyze data by city

city_yn = input('Would you like to view data by city? (Y/N)').upper()

if city_yn == 'Y' or input_yn == 'YES':
    input_city = input('Please enter the city you would like to receive data for:').upper()
    filtered_data_city_pre = df[df['PHYSICAL_CITY']==input_city]
    filtered_data_city_pre = filtered_data_city_pre.groupby('Year')
    filtered_data_city = filtered_data_city_pre['Total_sale_Price'].mean()
    filtered_data_city.plot()
    z.plot()

else:
    pass