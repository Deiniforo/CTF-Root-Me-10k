
## Write Up RPN. I solved the challenge in Python with the code described below.

# The description of the challenge is as follows:

# Who needs parentheses when you can use Jan's RPN to get an unambiguous formula?
# Author : Elf#4541
# nc ctf10k.root-me.org 8002

# To solve the challenge we must connect to ctf10k.root-me.org using netcat.
# Once connected, the server sends us messages like this:
#_______________________________________________________________________________________________________#
# Can you solve this for me?                                                                            #
# 819 620 41 880 522 - + 317 x - 22 626 37 x 679 + + 520 668 6 776 + + 426 + + 402 941 - 601 + x x x +  #
# >                                                                                                     #
#_______________________________________________________________________________________________________#

# From the description of the challenge, we know that it is Reverse Polish Notation.
# All that remains is to code an algorithm to calculate the given equation.
# To understand how this notation works, I took a look at wikipedia: https://en.wikipedia.org/wiki/Reverse_Polish_notation
# The implementation is very simple, thanks to the fact that no parentheses are used. We just use a stack.


import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('ctf10k.root-me.org', 8002))

messagenumero=1
while True:
    # We retrieve the message from the server.
    message_serveur=str(s.recv(2048).decode('utf-8')).split("\n")
    print('Server:', message_serveur)
    # We isolate the equation from the rest of the message
    equation=message_serveur[min(messagenumero,2)].split(" ")
    messagenumero+=1
    Pile=list()

    # The result is calculated. If the element "el" of the equation is a number, we add it to the end of the stack.
    # If it is an operation sign (+,-,x or /) we remove the last two elements from the stack and perform the operation.
    # Then we add the result of this operation to the stack.
    for el in equation:
        if el not in "+-x/":
            Pile.append(int(el))
        else:
            if el=="+":
                resultat=Pile.pop(-1)
                resultat+=Pile.pop(-1)
                Pile.append(resultat)
            elif el=="-":
                resultat=-Pile.pop(-1)
                resultat+=Pile.pop(-1)
                Pile.append(resultat)
            if el=="x":
                resultat=Pile.pop(-1)
                resultat*=Pile.pop(-1)
                Pile.append(resultat)
            if el=="/":
                resultat=Pile.pop(-1)
                resultat/=Pile.pop(-1)
                Pile.append(resultat)

    # We send the result of the equation to the server.
    print('Client: ', Pile[0])
    print(" ")
    s.send(bytes(str(Pile[0])+ '\n', 'ascii'))
s.close()

# We got the flag :
# RM{Luk4s13w1cz_w0uld_b3_pr0ud}