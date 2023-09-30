''' Essa classe é a responsável por guardar toda a informação sobre o estado atual do jogo,
e também é responsável por determinar os movimentos válidos do jogo '''

import math
import copy


class GameState():
    def __init__(self):
        # A tábua é possui lista de 8x8 e cada casa possui um elemento de dois caractere
        # O primeiro caractere representa a cor da peça "W" para white(Branco) e "B" para Black(Preto)
        # O segundo caractere representa o tipo da peça nas seguinte ordem: Torre, Cavalo, Bispo, Rainha, Rei, Bispo, Cavalo, Torre
        # '--' significa espaço vazio
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.whiteToMove = True
        self.moveLog = []
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

    def makeMove(self, move): # Faz os movimentos
        # fazendo o primeiro quadrado começar vazio
        self.board[move.startRow][move.startCol] = '--'
        # movendo a peça
        self.board[move.endRow][move.endCol] = move.pieceMoved
        # armazenando os movimentos gerados pelos jogadores
        self.moveLog.append(move)
        # mudando o turno
        self.whiteToMove = not self.whiteToMove


    def undoMove(self): #desfazendo o movimento
        if len(self.moveLog) != 0: # certificando que tem um movimento para desfazer
            move = self.moveLog.pop() # voltando a açao
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            # trocando o turno
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self): # todos os movimentos validos
        moves = self.getAllPossibleMoves()
        return moves


    def getAllPossibleMoves(self):  # todos os movimentos possiveis
        moves = []
        for r in range(len(self.board)):  # numeros de linhas
            for c in range(len(self.board[r])):  # numeros de coluna da linha
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves
    '''
    obtendo todos os movimentos das peças, sua linha e coluna e adicionando esse movimento na lista
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r - 1][c] == "--":
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # captura para esquerda
                if self.board[r - 1][c - 1][0] == 'b':  # peça inimiga para capturar
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:  # captura para direita
                if self.board[r - 1][c + 1][0] == 'b':  # peça inimiga para capturar
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:  # Movimento do peão preto
            if self.board[r + 1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:  # captura para esquerda
                if self.board[r + 1][c - 1][0] == 'w':  # peça inimiga para capturar
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:  # captura para direita
                if self.board[r + 1][c + 1][0] == 'w':  # peça inimiga para capturar
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) #cima, baixo, direita, esquerda
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions :
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # no tabuleiro
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # espaço vazio valido
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: # peça inimiga valida
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: # peça aliada (invalida)
                        break
                else: # fora do tabuleiro
                    break


    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, -1), (1, -1), (1, 1)) # 4 diagonais
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # no tabuleiro
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # espaço vazio valido
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # peça inimiga valida
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # peça aliada (invalida)
                        break
                else:  # fora do tabuleiro
                    break

    def getQueenMoves(self, r, c, moves):
        pass

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol <8:  # no tabuleiro
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # nao é uma peça aliada
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getKingMoves(self, r, c, moves):
        pass

    def getCastleMoves(self, r, c, moves):
        pass

    def getKingsideCastleMoves(self, r, c, moves):
        pass

    def getQueensideCastleMoves(self, r, c, moves):
        pass



class Move():
    # Numerando as linhas e colunas de 1 a 8
    ranksToRows = {"1":7,"2":6,"3":5,"4":4,
                   "5":3,"6":2,"7":1,"8":0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    # Mapeando as colunas de A a H
    filesToCols = {"a":0,"b":1,"c":2,"d":3,
                   "e":4,"f":5,"g":6,"h":7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    
    def __init__(self, startSq, endSq, board):
        # começo e fim da localizaçao/quadrado
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        # Onde a peça estava
        self.pieceMoved = board[self.startRow][self.startCol]
        # Onde a peça será movida
        self.pieceCaptured = board[self.endRow][self.endCol]
        # comparando os movimentos
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)

    # igualdade do objeto da class move
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
    
    # Essa função retorna a posição da casa e da coluna
    def getChessNot(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


