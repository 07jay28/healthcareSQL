import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

def create_numbers():
    for i in range(10):
        print(i)

    print("printing complete")

def toBeImplemented():
    # this function will be used for something
    # perhaps for commits
    return 0

def medicalConditions(cursor):
    conditions = """SELECT Medical_Condition, COUNT(*) AS Total_Patients
                  FROM healthcare 
                  Group BY Medical_Condition 
                  Order BY Total_Patients DESC"""

    cursor.execute(conditions)
    data = cursor.fetchall()
    for info in data:
        plt.bar(info[0], info[1], color='green')
        plt.text(info[0], info[1], info[1])

    plt.ylim(9000, 10000)
    plt.title('Medical Condition Count')
    plt.xlabel('Medical Condition')
    plt.ylabel('Number of Patients')
    plt.show()

def medicineConditionRelation(cursor):
    query = """SELECT Name, Medical_Condition, Medication 
                FROM healthcare 
                GROUP BY Medication"""

    cursor.execute(query)
    data = cursor.fetchall()
    print(data)


conn = sqlite3.connect('healthcare.db')
cursor = conn.cursor()
medicalConditions(cursor)
# medicineConditionRelation(cursor)
conn.close()

