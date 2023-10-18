import threading
import socket

HOST = '127.0.0.1'
PORT = 5555
clients = []


class socketClient:

    def __init__(self) -> None:

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.boards = [
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],]
        self.whiteToMove = True
        self.player = ''
        self.turn = True

        try:
            self.client.connect((HOST, PORT))
        except:
            return print('\nNão foi possívvel se conectar ao servidor!\n')

        print('\nConectado')

        board = eval(self.client.recv(4096).decode('utf-8'))
        self.boards = board

        self.player = self.client.recv(4096).decode('utf-8')
        if self.player != '0':
            self.whiteToMove = False
            self.turn = False
        print(self.player)

        leitor = threading.Thread(target=self.receiveMessages)
        leitor.start()

    def receiveMessages(self):
        while True:

            try:
                board = eval(self.client.recv(4096).decode('utf-8'))
                self.boards = board
                if self.boards == board:
                    print("ok")
                self.turn = not self.turn

            except:
                print('\nNão foi possível permanecer conectado no servidor!\n')
                print('Pressione <Enter> Para continuar...')
                self.client.close()
                break

    def attBoard(self, board):
        try:
            tabua = str(board).encode()
            self.client.send(tabua)
        except:
            return "fora de conexão"

    def close(self):
        self.client.close()
