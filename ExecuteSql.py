import mysql.connector
import pandas
import socketserver
import datetime
from http.server import BaseHTTPRequestHandler
from collections import defaultdict

def getPMRReport():
    print("Prepare to connect to database...")
    cnx = mysql.connector.connect(user='retainread', password='Letmein123', host='9.21.59.214', database='ccwinextension')
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
    #for (SHORT_NAME, Outstanding, Closed, New_incoming) in cursor:
    s = [] #Empty list
    for row in result:
        r = []
        r.append(row)
        d = {} #Empty dictionary

        d["OWNER"] = r[0][0]
        d["Outstanding"] = r[0][1]
        d["Closed"] = r[0][2]
        d["Incoming"] = r[0][3]
        s.append(d)

        #print(row)
    cursor.close()
    cnx.close()

    dd["Version"]="1.0"
    dd["CaseList"]=s
    dd["Update"]=datetime.datetime.now();
    print(dd)

    Table = pandas.DataFrame(s,columns=["OWNER","Outstanding","Closed","Incoming"])
    #Table.to_json("c:\\my.json")
    #print(Table)
    print(s)
    print(type(Table))
    #return s
    return Table


class MyHandler(BaseHTTPRequestHandler):

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(self):
        if self.path == '/getPMR':
            # getPMRReport()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b'<html><head><title>Title goes here.</title></head>')
            self.wfile.write(b'<body>')
            for index, row in getPMRReport().iterrows():
                self.wfile.write(b'<p>%s</p>' % row)
            self.wfile.write(b'</body></html>')

try:
    httpd = socketserver.TCPServer(("",8999), MyHandler)
    httpd.serve_forever()
except KeyboardInterrupt:
    print('^C received, shutting down server')
    httpd.socket.close()

def main():
    getPMRReport()

if __name__ == "__main__":
        main()