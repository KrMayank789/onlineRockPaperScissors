
import socket
from _thread import *
import pickle
from game import Game

#socket and _thread handle connections to our server


server = "192.168.43.108"

port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))


except socket.error as e:
    str(e)

s.listen(2) #detemines the number of connections to be connected
print("Waiting for a connection, Server Connected...")

connected = set()
games = {}
idCount = 0






def threaded_client(conn, p, gameId):#to get the information of which client is playing which game
    global idCount
    conn.send(str.encode(str(p)))#to identify if its p1 or p2

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()#4096 in case we are sending more information at a time
            # *it can be increased if any ran out of input error occured

            if gameId in games:
                game = games[gameId]#checks if the gamed is alive or not

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()

                    elif data != "get":
                        game.player(p, data)

                    reply = game
                    conn.sendall(pickle.dumps(reply))

            else:
                break
        except:
            break

    print("Lost connection")
    print("CLosing Game", gameId)
    try:
        del games[gameId]
    except:
        pass

    idCount -= 1
    conn.close()




while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount-1)//2 # every people connected to the server we are gonna have half of the games
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Wait,A new game is being created.....")
    else:
        games[gameId].ready = True
        p = 1



    start_new_thread(threaded_client, (conn, p, gameId))
