import socket


#The server sends messages like this:
#___________________________________________________________________________________________________________#
# Server: Hello there! I need some help for my homework, pleeeease.                                         #
# [1/60] Here's my graph's adjacency list, can you tell me if I can reach node 3 from 7 please? (yes / no)  #
# Node 0 has a directed edge to : 1                                                                         #
# Node 1 has a directed edge to : 2, 3, 5                                                                   #
# Node 2 has a directed edge to : 4                                                                         #
# Node 3 has no directed edge                                                                               #
# Node 4 has a directed edge to : 2, 6                                                                      #
# Node 5 has no directed edge                                                                               #
# Node 6 has no directed edge                                                                               #
# Node 7 has a directed edge to : 0, 8                                                                      #
# Node 8 has a directed edge to : 4, 7                                                                      #
#___________________________________________________________________________________________________________#




#___________________________________________________________________________________________________________#
# In this case, the graph is like this :                                                                    #
#                                                                                                           #
#        3             6                                                                                    #
#        ^             ^                                                                                    #
#        |             |                                                                                    #
# 5 <--- 1 ---> 2 <==> 4                                                                                    #
#        ^             ^                                                                                    #
#        |             |                                                                                    #
#        0 <--- 7 <==> 8                                                                                    #
#                                                                                                           #
# We need to find out if there is a path between two points of this graph.                                  #
# In the case of this example, a path does exist from 7 to 3. We can go for example through 7-> 0-> 1-> 3.  #
# So the answer to send to the server is "yes".                                                             #
#___________________________________________________________________________________________________________#

# Here's how I solved this challenge:

# I need a function that can tell me if a path exist or not:
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


# Now we just have to connect to the server, get the information and build the dictionary. Then send the answer.

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

    # Now that we have all the information, we calculate the answer to the question by using the booleen function.
    already_done_points=[]
    if booleen(entry_point,exit_point,D): reponse="yes"
    else: reponse="no"

    # We send the result to the server.
    print('Client: ', reponse)
    s.send(bytes(reponse+ '\n', 'ascii'))



# We got the flag :
# RM{34sy_d3pth_f1rst_s3arch}
