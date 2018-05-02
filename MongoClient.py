import pprint
import getpass

from pymongo import MongoClient

def handle_user_command(x,dbconnection):
    return{
        "cc" : "createNewCollection",
        "io" : "insertOne",
        "iow": "insertOneWrongRecord",
        "sc" : "showCollection",
        "dm" : "dummy",
    }.get(x, "Invalid command")

def RunMe():
    try:
        dbconnection = getDBConnection()

    except:
        print("!!!!!!!!!!!There is a problem when connect to mongodb, please check your password!!!!!!!!!!!!")
        raise SystemExit

    while 1:
        user_command = input("Please enter a command (cc/io/iow/sc/dm): ")
        execute_method = handle_user_command(user_command,dbconnection)
        if execute_method != "Invalid command":
            result = getattr(PlayCollection,execute_method)(dbconnection,"ekcollection")
            print("Command run successfully, exit message is {0}".format(result))
        else:
            print(execute_method)


    print("Done")


def getDBConnection():
    # getpass will not work in IDE environment but works in jupyter
    passwd = getpass.getpass("Enter password")
    client = MongoClient('mongodb://erikwang:{0}@35.196.213.79:27017/cards'.format(passwd))
    dbclient = client.cards
    return dbclient

class PlayCollection(object):

    def createNewCollection(MongoClient,dummyarg):
        MongoClient.create_collection("ekcollection")

    def insertOne(MongoClient, mycollection):
        try:
            MongoClient[mycollection].insert_one({'name':'Erik Wang'})
        except:
            print("There is an error when insert")
            exit()

        print("Record with 1 field inserted into {0} Successfully".format(mycollection))

    def insertOneWrongRecord(MongoClient,mycollection):
        try:
            MongoClient[mycollection].insert_one({'name':'Takumi','age':'20'})
        except:
            print("There is an error when insert")
            exit()

        print("Record with 2 fields inserted into {0} Successfully".format(mycollection))

    def showCollection(MongoClient,dummyarg):
        Collections = MongoClient.collection_names()
        if len(Collections) > 3:
            # Get a confirmation (y) from console
            flag = input(
                "Found more than one Collections in the database, input [y] if you want to show them all, otherwise I will exit....")
            if flag != 'y':
                print("{0} entered, bye".format(flag))
                raise SystemExit
        elif len(Collections) < 1:
            print("No collections in {1}".format(MongoClient.full_name))

        # To traversal all collections in a db
        for my_collection in Collections:
            print("Print one record in collection [{0}]".format(MongoClient[my_collection].full_name))
            print("Total records in collection <{0}>".format(MongoClient[my_collection].count()))
            # print(dbclient[my_collection].explain())

            pprint.pprint(MongoClient[my_collection].find_one())
            print("==================")

    def dummy(dummyarg0,dummyarg1):
        return 'Dummy'

if __name__ == "__main__":
    RunMe()
