# takes in the healthcare csv dataset and turns it into a db for sql
import pandas as pd
import sqlite3


def csvToDB(csvFile):
    dataFile = pd.read_csv(csvFile)
    # dataFile.info()

    tableName = "healthcare"
    columnTypes = ", ".join([f"{col.replace(' ', '_')} TEXT" for col in dataFile.columns])
    createTable = f"CREATE TABLE IF NOT EXISTS {tableName} ({columnTypes});"

    cursor = conn.execute(createTable)
    cursor.fetchall()

    cursor.execute('pragma table_info(healthcare);')
    print(cursor.fetchall())

    for index, row in dataFile.iterrows():
        values = ", ".join([f'"{row_item}"' for row_item in row])
        insertSQL = f"INSERT INTO {tableName} ({', '.join(dataFile.columns.str.replace(' ', '_'))}) VALUES ({values});"
        cursor.execute(insertSQL)

    print(dataFile.shape)
    cursor.execute("SELECT COUNT(*) FROM healthcare")
    print(cursor.fetchall())

    conn.commit()
    conn.close()


file = 'healthcare_dataset.csv'
conn = sqlite3.connect('healthcare.db')
cursor = conn.cursor()
csvToDB(file)