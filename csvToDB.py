# takes in the healthcare csv dataset and turns it into a db for sql
import pandas as pd
import sqlite3

def csvToDB(csvFile, cursor):
    dataFile = pd.read_csv(csvFile)

    tableName = "SeoulFloating"
    columnTypes = ", ".join([f"{col.replace(' ', '_')} TEXT" for col in dataFile.columns])
    createTable = f"CREATE TABLE IF NOT EXISTS {tableName} ({columnTypes});"

    cursor.execute(createTable)
    # cursor.fetchall()

    cursor.execute(f'pragma table_info({tableName});')
    # print(cursor.fetchall())

    for index, row in dataFile.iterrows():
        values = ", ".join([f'"{row_item}"' for row_item in row])
        insertSQL = f"INSERT INTO {tableName} ({', '.join(dataFile.columns.str.replace(' ', '_'))}) VALUES ({values});"
        cursor.execute(insertSQL)

    print(dataFile.shape)
    cursor.execute(f"SELECT COUNT(*) FROM {tableName}")
    print(cursor.fetchall())

    conn.commit()
    conn.close()


file = './2020 Covid Korea/SeoulFloating.csv'
conn = sqlite3.connect('KoreaCovidData/SeoulFloating.db')
cursor = conn.cursor()
csvToDB(file, cursor)