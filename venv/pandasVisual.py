#Run in Jupyter Notebooks

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mysql.connector
from collections import defaultdict
from time import gmtime, strftime

print("Prepare to connect to Dispatcher database...")
cnx = mysql.connector.connect(user='readonly', password='readonly123', host='9.21.59.99',
                              database='pmrdispatcher')
cursor = cnx.cursor()
query = ("SELECT * FROM pmrdispatcher.sym_cws_na_weekly \
        Where OwnerName in ('Jonas Welcome','Henry Li','Erik Wang', 'Geoffrey Young','Jun Zhu','Steve Lee','Adrian Barbur','Aditya Ramaraju','Mona Aggarwal')\
        Order by OwnerName")

cursor.execute(query)
result = cursor.fetchall()
print('The size of the result is %s' % result.__sizeof__())
s = []  # Empty list
dfindex = []  # For the index of the collection
for row in result:
    r = []
    r.append(row)

    d = {}  # Empty dictionary
    d["OWNER"] = r[0][0]
    d["Outstanding"] = r[0][1]
    d["Closed"] = r[0][2]
    d["Incoming"] = r[0][3]
    # S is the list which contains all engineers' records
    s.append(d)
    dfindex.append(d["OWNER"])
    # print(row)

cursor.close()
cnx.close()
# print(d)
# Setuo the json format
dd = defaultdict(list)
dd["Version"] = "1.0"
dd["CaseList"] = s
dd["Update"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())

print(dfindex)
# In case we need a DataFrame here...
Table = pd.DataFrame(s, index=dfindex, columns=['OWNER', 'Outstanding', 'Closed', 'Incoming'])
# Generate a json file
# Table.to_json("c:\\my.json")


# print(Table.to_string(index=False))
print(Table)

# Table.plot(kind='bar')
Table.plot.bar(stacked=True) # Visualize the Dataframe


'''
ts = pd.Series(np.random.randn(5000), index=pd.date_range('1/1/2000', periods=5000))
ts = ts.cumsum()
ts.plot()
'''

