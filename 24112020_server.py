import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 52472        # Port to listen on (non-privileged ports are > 1023)
CLIENTS = []
BOARD = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
PLAYER_PLAYING = 0

def send_all(msg):
    for client in CLIENTS:
        client.send(msg.encode())

def convert_board_to_string():
    msg = "BOARD"
    for i in range(3):
        for j in range(3):
            msg += str(BOARD[i][j])
    return msg

def get_row_col():
    global PLAYER_PLAYING
    for client in CLIENTS:
        if CLIENTS[PLAYER_PLAYING] == client:
            client.send("PLAY".encode())
        elif CLIENTS[PLAYER_PLAYING-1] == client or CLIENTS[PLAYER_PLAYING+1] == client:
            client.send("WAIT".encode())
    row = CLIENTS[PLAYER_PLAYING].recv(1024).decode()
    col = CLIENTS[PLAYER_PLAYING].recv(1024).decode()
    if PLAYER_PLAYING == 0:
        PLAYER_PLAYING = 1
    elif PLAYER_PLAYING == 1:
        PLAYER_PLAYING = 0
    return row,col
    
    

def update_board(row, col):
    if PLAYER_PLAYING == 0:
        sign = 1
    else:
        sign = 2
    BOARD[row-1][col-1] = sign
        


def game_loop_server():
    game_play = True
    while game_play:
        send_all("PLAY")
        for client in CLIENTS:
            client.recv(1024).decode()          
        row_col = get_row_col()
        row = int(row_col[0])
        col = int(row_col[1])
        update_board(row, col)
        str_board = convert_board_to_string()
        send_all(str_board)
        for client in CLIENTS:
            client.recv(1024).decode() 
    send_all("DONT PLAY")


   
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create TCP socket
    s.bind((HOST, PORT)) # bind the socket with the IP and the port
    s.listen() # open the socket for client connections
    print("waiting for clients...")
    client_connection1, addr = s.accept() # wait until client will connect
    CLIENTS.append(client_connection1)
    name1 = client_connection1.recv(1024).decode()
    print(f"{name1} is connected")
    client_connection1.send("WAIT".encode())
    client_connection2, addr = s.accept()  # wait until client will connect
    CLIENTS.append(client_connection2)
    name2 = client_connection2.recv(1024).decode()
    print(f"{name2} is connected")
    send_all("START")
    print("STRATING GAME")
    game_loop_server()

    
    



    #s.close()


main()