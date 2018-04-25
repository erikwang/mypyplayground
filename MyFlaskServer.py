from flask import Flask, request
from flask_restful import Resource, Api
import mysql.connector
import pandas
from time import gmtime, strftime
from collections import defaultdict

app = Flask(__name__)
api = Api(app)

class WhateverToShow(Resource):
    def get(self):
        return {'TheName':'Erik'}

class DefaultURI(Resource):
    def get(self):
        return {'Message':'Welcome to the jungle'}


class CaseReport(Resource):
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



api.add_resource(WhateverToShow,'/whatever')
api.add_resource(DefaultURI,'/')
api.add_resource(CaseReport,'/case')

if __name__ == '__main__':
     app.run(port= 5002)