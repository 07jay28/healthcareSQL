# Thanks Jalen. Uncle Mike appreciates learning Git with you.
# Removed comments

# Comment in development branch for PR rebase practice

# python file for the Korean Covid data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import sqlite3

# this function analyzes the data in regards to cases for the top 5 provinces
def CasesDataPerProvince(cursor):
    q = """ SELECT province, SUM(confirmed) as Total_Confirmed
            FROM Cases
            GROUP BY province
            ORDER BY Total_Confirmed DESC
            LIMIT 5"""
    cursor.execute(q)
    data = cursor.fetchall()

    for info in data:
        plt.bar(info[0], info[1])
        plt.text(info[0], info[1], info[1])

    plt.title("Top 5 Provinces with Confirmed Cases")
    plt.xlabel("Provinces")
    plt.ylabel("Cases")
    plt.savefig("./Outputs/Confirmed Cases by Province.png")
    plt.show()

def PatientInfo(cursor):
    queryMale = """SELECT age, count(age) as Number_of_Patients_Age_Group
                    FROM PatientInfo
                    WHERE sex='male' AND age!='nan' AND age!='100s' 
                    GROUP BY age
                    ORDER BY age ASC"""
    cursor.execute(queryMale)
    maleData = cursor.fetchall()

    queryFemale = """SELECT age, count(age) as Number_of_Patients_Age_Group
                        FROM PatientInfo
                        WHERE sex='female'  AND age!='nan' AND age!='100s'
                        GROUP BY age 
                        ORDER BY age ASC"""
    cursor.execute(queryFemale)
    femaleData = cursor.fetchall()

    maleCount, femaleCount = [], []
    ageGroup = []
    for row in maleData:
        maleCount.append(row[1])
        ageGroup.append(row[0])

    for row in femaleData:
        femaleCount.append(row[1])

    N = len(ageGroup)
    ind = np.arange(N)
    width = 0.35

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    rects1 = ax.bar(ind, maleCount, width, color='lightblue', label="Men")
    rects2 = ax.bar(ind+width, femaleCount, width, color='pink', label="Women")

    ax.set_title("Patient Age Groups")
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Number of Patients")
    ax.set_xticks(ind+width/2)
    t = tuple(a for a in ageGroup)
    
    ax.set_xticklabels(t)
    plt.legend()
    plt.savefig("./Outputs/Patient Age Groups.png")
    plt.show()

def plotPatientLatLong(cursor):
    koreaMap = gpd.read_file("./KoreaMap/kr.shp")
    fig,ax = plt.subplots()

    query = """SELECT latitude, longitude
               FROM Cases
               WHERE latitude!='-' AND longitude!='-'"""

    cursor.execute(query)
    data = cursor.fetchall()
    lat,long = [], []
    for row in data:
        lat.append(row[0])
        long.append(row[1])

    df = pd.DataFrame({'latitude':lat, 'longitude':long})
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
    ax = gdf.plot(alpha=1,color='green',zorder=1,marker='o',markersize=3)
    ax.set_facecolor('lightblue')
    koreaMap.plot(cmap='YlOrBr', ax=ax,zorder=0)

    ax.set_title("Cases Location")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    plt.savefig("./Outputs/PatientLatLong.png")
    

# function to go through search trend and look at data changes for each symptom and plot on a pie char
def searchTrend(cursor):
    query = """ SELECT *
                FROM SearchTrend"""

    cursor.execute(query)
    data = cursor.fetchall()
    for row in data:
        date = row[0]
        cold = row[1]
        flu = row[2]
        pneum = row[3]
        covid = row[4]

    # plot a pie chart interactive for each date
    # can also have a functionality for looking at a specific month only
    return 0


# database connections
CasesConn = sqlite3.connect('./KoreaCovidData/Case.db')
PatientInfoConn = sqlite3.connect('./KoreaCovidData/PatientInfo.db')
SearhConn = sqlite3.connect('./KoreaCovidData/SearhTrend.db')

# database cursors
CaseCursor = CasesConn.cursor()
PatientCursor = PatientInfoConn.cursor()
SearhCursor = SearhConn.cursor()

# functions
CasesDataPerProvince(CaseCursor)
PatientInfo(PatientCursor)
plotPatientLatLong(CaseCursor)

CasesConn.close()
PatientInfoConn.close()
SearhConn.close()