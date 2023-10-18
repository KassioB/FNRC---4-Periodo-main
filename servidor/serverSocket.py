import threading
import socket


HOST = '127.0.0.1'
PORT = 5555
clients = []
board = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bR", "bR"],
    ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]


def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print("Servidor iniciado")
        server.listen()
    except:
        return print('\nNão foi possível iniciar o servidor!\n')

    while True:
        client, addr = server.accept()
        clients.append(client)

        tabua = str(board).encode()
        client.send(tabua)

        client.send(str(clients.index(client)).encode())

        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()


def messagesTreatment(client):
    bolean = True
    while True:
        try:
            if bolean:
                board = eval(clients[0].recv(4096).decode('utf-8'))
                attboard = str(board).encode()
                print("recebido player1")
                broadcast(attboard)
                bolean = not bolean
            else:
                board = eval(clients[1].recv(4096).decode('utf-8'))
                attboard = str(board).encode()
                print("recebido player 2")
                broadcast(attboard)
                bolean = not bolean

        except:
            print("Usuário desconectado")
            deleteClient(client)
            break


def broadcast(board):
    for clientItem in clients:
        try:
            clientItem.send(board)
            print("Enviado!")
        except:
            deleteClient(clientItem)


def deleteClient(client):
    clients.remove(client)


if __name__ == "__main__":
    main()
