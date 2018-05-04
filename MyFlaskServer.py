import os
from flask import Flask
from flask_restful import Resource, Api
from flask_socketio import SocketIO
import mysql.connector
from time import gmtime, strftime
from collections import defaultdict

#For Pandas Visualization
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np




app = Flask(__name__)
api = Api(app)
socketio = SocketIO(app)



class WhateverToShow(Resource):
    def get(self):
        return {'TheName':'Erik'}

class DefaultURI(Resource):
    def get(self):
        return {'Message':'Welcome to the jungle'}


#Access to old Retain Mysql instance for PMR.
class PMRReport(Resource):
    def get(self):
        print("Prepare to connect to database...")
        cnx = mysql.connector.connect(user='retainread', password='Letmein123', host='9.21.59.214',
                                      database='ccwinextension')
        cursor = cnx.cursor()

        query = "select team.SHORT_NAME, IFNULL(opened.cc,0) Outstanding, IFNULL(closed.cc,0) Closed, IFNULL(newopened.cc,0) New_incoming \
                 From \
                 (SELECT SHORT_NAME,USER_RETAINID \
                    from ccwinextension.t_s_user \
                    where USER_RETAINID in ('049568', '048595','048196','046450','045519','044576','042371','040951','040785')) team \
                 LEFT JOIN \
                 (SELECT OWNER, OWNER_RETAINID, count(*) cc FROM ccwinextension.t_d_pmr \
                    where CLOSE_DATE > DATE_SUB(CURDATE(), INTERVAL 5 DAY) and team_id like '%[8]%' and QUEUE = 'SYMNA' \
                    group by OWNER_RETAINID) closed \
                    ON (team.USER_RETAINID = closed.OWNER_RETAINID) \
                 LEFT JOIN \
                (SELECT OWNER, OWNER_RETAINID, count(*) cc FROM ccwinextension.t_d_pmr \
                    where CLOSE_DATE is null and team_id like '%[8]%' and QUEUE = 'SYMNA' \
                    group by OWNER_RETAINID) opened \
                ON (team.USER_RETAINID = opened.OWNER_RETAINID) \
                LEFT JOIN \
                (SELECT OWNER, OWNER_RETAINID, count(*) cc FROM ccwinextension.t_d_pmr \
                    where OPEN_DATE > DATE_SUB(CURDATE(), INTERVAL 5 DAY)and team_id like '%[8]%' and QUEUE = 'SYMNA' \
                    group by OWNER_RETAINID) newopened \
                ON (team.USER_RETAINID = newopened.OWNER_RETAINID) \
                ORDER BY SHORT_NAME"
        '''
        query = ("SELECT * from ccwinextension.t_s_user")
        '''

        cursor.execute(query)
        result = cursor.fetchall()
        print('The size of the result is %s' % result.__sizeof__())

        print("executing...")

        dd = defaultdict(list)

        s = []  # Empty list
        for row in result:
            r = []
            r.append(row)
            d = {}  # Empty dictionary
            d["OWNER"] = r[0][0]
            d["Outstanding"] = r[0][1]
            d["Closed"] = r[0][2]
            d["Incoming"] = r[0][3]
            #S is the string which contains all case records
            s.append(d)
            # print(row)
        cursor.close()
        cnx.close()

        print(d)

        dd["Version"] = "1.0"
        dd["CaseList"] = s
        dd["Update"] = strftime("%Y-%m-%d %H:%M:%S",gmtime())

        Table = pandas.DataFrame(s, columns=['OWNER', 'Outstanding', 'Closed', 'Incoming'])
        #Generate a json file
        #Table.to_json("c:\\my.json")

        #Output to a dictionary for Flask to transform to json
        #return Table.to_dict('index')

        #Return the dictionary directly
        #DD has 3 keys: version, CaseList and Update. CaseList is a list of every record.
        return dd


#Access to new Dispatcher mysql instance for cases
class CaseReport(Resource):
    def get(self):
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
        print("executing...")

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
            #S is the string which contains all case records
            s.append(d)
            dfindex.append(d["OWNER"])
            # print(row)
        cursor.close()
        cnx.close()

        #print(d)

        #Setuo the json format
        dd = defaultdict(list)
        dd["Version"] = "1.0"
        dd["CaseList"] = s
        dd["Update"] = strftime("%Y-%m-%d %H:%M:%S",gmtime())

        #In case we need a DataFrame here...
        Table = pd.DataFrame(s, index=dfindex, columns=['OWNER', 'Outstanding', 'Closed', 'Incoming'])
        Table.plot.bar(stacked=True)

        #Generate a json file
        #Table.to_json("c:\\my.json")

        #Return the dictionary directly
        #DD has 3 keys: version, CaseList and Update. CaseList is a list of every record.
        return dd

class CaseReportDemo(Resource):
    def get(self):
        dd = defaultdict(list)
        r = []
        for i in range(1,3):
            r.append([strftime("%Y-%m-%d %H:%M:%S",gmtime()),i])
        dd["Version"] = "Random"
        dd["CaseList"] = r
        return dd


api.add_resource(WhateverToShow,'/whatever')
api.add_resource(DefaultURI,'/')
api.add_resource(PMRReport,'/pmr')
api.add_resource(CaseReport,'/case')
api.add_resource(CaseReportDemo,'/casedemo')


if __name__ == '__main__':
    print("Http server is ready {0}".format(api.resources))

    port1 = int(os.environ.get('PORT', 5002))

    #Following two lines also worked to start the server
    #app.run(host='0.0.0.0',port = port1)
    # app.run(host='0.0.0.0',port= 5002)

    #Try to fix an issue(but didn't work) that the URI can be retrived with curl but when use firefox, the connections was reset...
    socketio.run(app, host='0.0.0.0', port=port1)