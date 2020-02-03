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
plt.ylabel('Price in Dollars')
plt.title('Number of Residential Home Sales per Year')
plt.legend()
plt.show()

z.plot()
plt.ylabel('Price in Dollars')
plt.title('Average Price of Residential Homes per Year')
plt.legend()
plt.show()

# Function to analyze data by zipcode

def zipFunc(zip):
        input_zip = int(zip)
        filtered_data_zip_pre = df[df['PHYSICAL_ZIP_CODE']==input_zip]
        filtered_data_zip_pre = filtered_data_zip_pre.groupby('Year')
        filtered_data_zip = filtered_data_zip_pre['Total_sale_Price'].mean()
        filtered_data_zip.plot()
        z.plot()
        plt.show()

# # Function to analyze data by street

def streetFunc(street, prefix=' '):
        if prefix == ' ':
            filtered_data_pre = df[df["Street_Name"]==input_street]
            filtered_data_pre = filtered_data_pre.groupby('Year')
            filtered_data = filtered_data_pre['Total_sale_Price'].mean()
            filtered_data.plot()
            z.plot()
            plt.show()
        else:
            filtered_data_prefix = df[df["Street_Prefix"]==prefix]
            filtered_data_pre = filtered_data_prefix[filtered_data_prefix["Street_Name"]==street]
            filtered_data_pre = filtered_data_pre.groupby('Year')
            filtered_data = filtered_data_pre['Total_sale_Price'].mean()
            filtered_data.plot()
            z.plot()
            plt.show()

# # Function to analyze data by city

def cityFunc(city):
        input_city = city
        filtered_data_city_pre = df[df['PHYSICAL_CITY']==input_city]
        filtered_data_city_pre = filtered_data_city_pre.groupby('Year')
        filtered_data_city = filtered_data_city_pre['Total_sale_Price'].mean()
        filtered_data_city.plot()
        z.plot()
        plt.show()