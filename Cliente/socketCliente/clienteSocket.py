import threading
import socket

HOST = '127.0.0.1'
PORT = 5555
clients = []


class socketClient:

    def __init__(self) -> None:

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.board = [
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
        self.playerClicks = []

        try:
            self.client.connect((HOST, PORT))
        except:
            return print('\nNão foi possívvel se conectar ao servidor!\n')

        print('\nConectado')

        self.player = self.client.recv(4096).decode('utf-8')
        if self.player != '0':
            self.turn = False

        board = eval(self.client.recv(4096).decode('utf-8'))
        self.board = board

        leitor = threading.Thread(target=self.receiveMessages)
        leitor.start()

    def receiveMessages(self):
        while True:

            try:
                board = eval(self.client.recv(4096).decode('utf-8'))
                self.playerClicks = board
                print('recebido')

            except:
                print('\nNão foi possível permanecer conectado no servidor!\n')
                print('Pressione <Enter> Para continuar...')
                self.client.close()
                break

    def clicks(self, board):
        try:
            tabua = str(board).encode()
            self.client.send(tabua)
            print('Enviado')
        except:
            return "fora de conexão"

    def close(self):
        self.client.close()
