import socket


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 52472        # The port used by the server
S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def print_board(board):
    final_board = ""
    counter = 1
    for sign in board:
        if counter == 4 or counter == 7:
            final_board += "\n"
        if sign == "0":
            final_board += "_"
            counter += 1
        elif sign == "1":
            final_board += "X"
            counter += 1
        elif sign == "2":
            final_board += "O"
            counter += 1
    return final_board   

def send_row_col():
    play_or_wait = S.recv(1024).decode()
    if play_or_wait == "PLAY":
        print("your turn")
        row = int(input("row - "))
        col = int(input("col - "))
        while row not in range(1,4) or col not in range(1,4):
            print("unvalid row or column")
            row = int(input("row - "))
            col = int(input("col - "))
        S.send(str(row).encode())
        S.send(str(col).encode())
            
    elif play_or_wait == "WAIT":
        print("wait for your turn")

def game_loop_client():
    while True:
        game_play = S.recv(1024).decode()
        if game_play == "PLAY":
            S.send("PLAYING".encode())
            send_row_col()
            board = S.recv(1024).decode()
            S.send("BOARD ARRIVED".encode())
            print(print_board(board))
        elif game_play == "GAME OVER":
            print("game over")
            break


def main():
    S.connect((HOST, PORT))
    name = input("enter your name: ")
    S.send(name.encode()) # send hello after converting it to bytes
    start_or_wait = S.recv(1024).decode()
    if start_or_wait == "WAIT":
        print("waiting for second player")
        start_or_wait = S.recv(1024).decode()
    if start_or_wait == "START":
        print("starting the game")
        game_loop_client()
    

    

    #s.close()

main()

