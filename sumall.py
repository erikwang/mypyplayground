from functools import reduce

def main():
    #aa = [1,2,3,4,5,6,7,8]
    aa=(1,2,3,4,5,6,7,8,9)
    print (aa, type(aa))
    print(reduce(lambda x,y:(x+y),aa))

if __name__ == "__main__":
        main()
