import mysql.connector
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
print(result.__sizeof__())

print("executing...")

#for (SHORT_NAME, Outstanding, Closed, New_incoming) in cursor:
for row in result:
    print("..")
#    print("{},{},{},{}".format(SHORT_NAME, Outstanding, Closed, New_incoming))
    print(row)
cursor.close()
cnx.close()