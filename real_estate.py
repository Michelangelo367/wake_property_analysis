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

# Function to analyze data

def propAnalysis(field_name):
    input_yn = input('Would you like to view data by ' + field_name.lower() + '? (Y/N) ').upper()
    try:
        if input_yn == 'Y' or input_yn == 'YES':
            inputvar = int(input('Please enter the ' + field_name.lower() + ' you would like to receive data for: '))
            filtered_data_pre = df[df['PHYSICAL_ZIP_CODE']==inputvar]
            filtered_data_pre = filtered_data_pre.groupby('Year')
            filtered_data = filtered_data_pre['Total_sale_Price'].mean()
            filtered_data.plot()
            z.plot()
            plt.show()
            print('YOY Change is: ')
            var_assess_price = filtered_data_pre['Total_Assessed_Valuation'].mean()
            var_chart = filtered_data_pre['Total_sale_Price'].mean() / var_assess_price
            print(var_chart.pct_change(periods=2))
            
            var_assess = input('Would you like to view home price vs. assessed home price? (Y/N) ').upper()
            if var_assess == 'Y' or var_assess == 'YES':
                var_assess_price = filtered_data_pre['Total_Assessed_Valuation'].mean()
                print('Total Sale Price / Total Valuation Price: (Over 1 means the owner is paying above valuation, under 1 means the owner is paying below valuation.) ')
                var_chart = filtered_data_pre['Total_sale_Price'].mean() / var_assess_price
                print(var_chart)
        else:
            pass
    except:
        print('That is not valid. Please try again with a valid entry.')

# Charting by zip code, street, and city data

propAnalysis('PHYSICAL_ZIP_CODE')

propAnalysis("Street_Name")

propAnalysis('PHYSICAL_CITY')