import socket

HOST = '10.100.102.28'  # Standard loopback interface address (localhost)
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

def is_game_over(): # return True if game is over and False if not
    empty_places_counter = 0
    for i in BOARD:
        in_row = 0
        first_sign = ""
        for j in i:
            if first_sign == "" and j != 0:
                first_sign = j
            if first_sign == j:
                in_row += 1
            if in_row == 3:
                return True            
            if j == 0:
                empty_places_counter += 1
            
    if empty_places_counter == 0:
        return True

    list_board = board_into_reg_list()
    if (list_board[0] == list_board[3] and list_board[3] == list_board[6] and list_board[6] != 0) or (list_board[1] == list_board[4] and list_board[4] == list_board[7] and list_board[7] != 0) or (list_board[2] == list_board[5] and list_board[5] == list_board[8] and list_board[8] != 0) or (list_board[0] == list_board[4] and list_board[4] == list_board[8] and list_board[8] != 0) or (list_board[2] == list_board[4] and list_board[4] == list_board[6] and list_board[6] != 0):
        return True

def board_into_reg_list():
    new_board = []
    for i in BOARD:
        for j in i:
            new_board.append(j)
    return new_board

def get_row_col():
    global PLAYER_PLAYING
    for client in CLIENTS:
        if CLIENTS[PLAYER_PLAYING] == client:
            client.send("PLAY".encode())
        elif CLIENTS[PLAYER_PLAYING-1] == client or CLIENTS[PLAYER_PLAYING+1] == client:
            client.send("WAIT".encode())
    row = CLIENTS[PLAYER_PLAYING].recv(1024).decode()
    col = CLIENTS[PLAYER_PLAYING].recv(1024).decode()

    return row,col
    
def change_turn():
    global PLAYER_PLAYING
    if PLAYER_PLAYING == 0:
        PLAYER_PLAYING = 1
    elif PLAYER_PLAYING == 1:
        PLAYER_PLAYING = 0

def check_place(row, col):
    if BOARD[row-1][col-1] == 0:
        return "empty"
    return "not empty"

def update_board(row, col):
    if PLAYER_PLAYING == 0:
        sign = 1
    else:
        sign = 2
    BOARD[row-1][col-1] = sign


def game_loop_server():
    game_play = True
    board_ready_to_send = False
    while game_play:
        if is_game_over():
            send_all("GAME OVER")
        else:   
            send_all("PLAY")
        for client in CLIENTS:
            client.recv(1024).decode()          
        row_col = get_row_col()
        row = int(row_col[0])
        col = int(row_col[1])
        is_empty = check_place(row, col)        
        while is_empty == "not empty":
            CLIENTS[PLAYER_PLAYING].send("PLACE FULL".encode())
            row_col = get_row_col()
            row = int(row_col[0])
            col = int(row_col[1])
            is_empty = check_place(row, col)
        if is_empty == "empty":
            update_board(row, col)
            CLIENTS[PLAYER_PLAYING].send("PLACED".encode()) 
            board_ready_to_send = True
        if board_ready_to_send:        
            str_board = convert_board_to_string()
            send_all(str_board)
        for client in CLIENTS:
            client.recv(1024).decode()
        change_turn()



   
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
    s.close()


main()