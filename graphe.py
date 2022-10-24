import socket



#___________________________________________________________________________________________________________#
# Server: Hello there! I need some help for my homework, pleeeease.                                         #
# [1/60] Here's my graph's adjacency list, can you tell me if I can reach node 7 from 19 please? (yes / no) #
# Node 0 has a directed edge to : 1, 6                                                                      #
# Node 1 has a directed edge to : 5, 16                                                                     #
# Node 2 has a directed edge to : 14, 15, 17, 19                                                            #
# Node 3 has a directed edge to : 13                                                                        #
# Node 4 has no directed edge                                                                               #
# Node 5 has no directed edge                                                                               #
# Node 6 has a directed edge to : 13, 16, 17                                                                #
# Node 7 has a directed edge to : 5, 19                                                                     #
# Node 8 has a directed edge to : 3                                                                         #
# Node 9 has a directed edge to : 6                                                                         #
# Node 10 has no directed edge                                                                              #
# Node 11 has a directed edge to : 3, 7, 17                                                                 #
# Node 12 has a directed edge to : 8, 17, 20                                                                #
# Node 13 has a directed edge to : 3, 7, 10, 17, 19, 20                                                     #
# Node 14 has a directed edge to : 2, 6, 9, 13, 17, 19, 20                                                  #
# Node 15 has no directed edge                                                                              #
# Node 16 has a directed edge to : 0, 3                                                                     #
# Node 17 has a directed edge to : 2, 4                                                                     #
# Node 18 has a directed edge to : 11, 15, 19                                                               #
# Node 19 has a directed edge to : 9, 20                                                                    #
# Node 20 has a directed edge to : 4                                                                        #
#___________________________________________________________________________________________________________#



# This function takes as input two point indices and a dictionary representing the links of the graph.
# It returns True if there is a path between the entry point and the exit point, False otherwise.
def booleen(entry,exit,D):
    global already_done_points
    already_done_points.append(entry)
    if entry==exit:
        return(True)
    else:
        if D[entry]==[]:
            return(False)
        else:
            bool=False
            for o in D[entry]:
                if o not in already_done_points:
                    bool=bool or booleen(o,exit,D)
            return(bool)

# connexion
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('ctf10k.root-me.org', 8001))

while True:
    # We retrieve the message from the server.
    message_serveur=str(s.recv(2048).decode('utf-8'))
    print('Server:', message_serveur)

    # We eliminate the parts of the message without useful information.
    message_beginning_index=0
    while message_serveur[message_beginning_index:message_beginning_index+18]!="please? (yes / no)":
        message_beginning_index+=1
    message=message_serveur[:message_beginning_index]
    Liste=message_serveur[message_beginning_index+18:].split("\n")[1:-1]



    message_end_index=0
    while message[message_end_index:message_end_index+4]!="/60]":
        message_end_index+=1
    message=message[message_end_index+4:].split(" ")

    # Now that the message is clean, we can extract the names of the two points we want to connect.
    exit_point=int(message[-4])
    entry_point=int(message[-2])

    # All that remains is to build a dictionary to represent the links between the points.
    # It is of the form D{P1:[P2,P3],P2:[]}. With this example we know that from P1 we can go to P2 or P3, but that P2 does not lead anywhere
    D={}
    for i in range(len(Liste)):
        chaine=Liste[i]
        if "has no directed edge" in chaine:
            D[i]=[]
        else:
            L=[]
            indice=0
            while chaine[indice]!=":":
                indice+=1
            chaine=chaine[indice+1:].split(",")
            for nb in chaine:
                L.append(int(nb))
            D[i]=L

    # Now that we have all the information, we calculate the answer to the question.
    already_done_points=[]
    if booleen(entry_point,exit_point,D): reponse="yes"
    else: reponse="no"

    # We send the result to the server.
    print('Client: ', reponse)
    s.send(bytes(reponse+ '\n', 'ascii'))



# We got the flag :
# RM{34sy_d3pth_f1rst_s3arch}
