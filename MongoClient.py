import pprint
import getpass

from pymongo import MongoClient

#getpass will not work in IDE environment but works in jupyter
passwd = getpass.getpass("Enter password")


try:
    client  = MongoClient('mongodb://erikwang:{0}@35.196.213.79:27017/cards'.format(passwd))
    dbclient = client.cards
    Collections = dbclient.collection_names()
except:
    print("!!!!!!!!!!!There is a problem when connect to mongodb, please check your password!!!!!!!!!!!!")
    raise SystemExit

#print(type(Collections))


#To get a single colleciton from databse cards
#Cards_collection = dbclient.MyHsCards

if len(Collections) > 1:
    #Get a confirmation (y) from console
    flag = input("Found more than one Collections in the database, input [y] if you want to show them all, otherwise I will exit....")
    if  flag != 'y':
        print("{0} entered, bye".format(flag))
        raise SystemExit
elif len(Collections) < 1:
    print("No collections in {1}".format(dbclient.full_name))

#To traversal all collections in a db
for my_collection in Collections:
    print("Print one record in collection [{0}]".format(dbclient[my_collection].full_name))
    print("Total records in collection <{0}>".format(dbclient[my_collection].count()))
    pprint.pprint(dbclient[my_collection].find_one())
    print("==================")


#for post in mycollection.find():
    #pprint.pprint(post)

print("Done")