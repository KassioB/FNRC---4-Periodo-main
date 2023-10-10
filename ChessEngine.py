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
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True
        self.moveLog = []
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)

        self.inCheck = False
        self.pins = []
        self.checks = []

    def makeMove(self, move):  # Faz os movimentos
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.board[move.startRow][move.startCol] = "--"
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove  # mudando os turnos

        # Melhorando o movimento do rei
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

    def undoMove(self):  # desfazendo o movimento
        if len(self.moveLog) != 0:  # certificando que tem um movimento para desfazer
            move = self.moveLog.pop()  # voltando a açao
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            # trocando o turno
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

    def getValidMoves(self):  # todos os movimentos validos (maquina)
        moves = []
        # Analisa todas as possibilidades de check
        self.inCheck, self.pins, self.checks = self.checksForPinsAndChecks()

        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]

        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]

        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                # Para bloquear o ckeck se você tiver uma peça aliada entre o inimigo e seu rei
                check = self.checks[0]  # informações do check
                checkRow = check[0]
                checkCol = check[1]
                # Peça inimiga que ameaça o check
                pieceCheking = self.board[checkRow][checkCol]
                validSquares = []  # casas em que a peça pode se mover

                # Se cavalo, captura o cavalo ou move o rei, outras peças também podem bloquear
                if pieceCheking == 'N':
                    validSquares[(checkRow, checkCol)]

                else:
                    for i in range(1, 8):
                        # Para onde o Rei deve se mover
                        validSquare = (
                            kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break

                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquare:
                            moves.remove(moves[i])

            else:  # Duas ameaças de check e o rei tem de mudar de casa
                self.getKingMoves(kingRow, kingCol, moves)

        else:  # Não está em check e todos os movimentos estão ok's
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

    def checksForPinsAndChecks(self):
        pins = []  # casas onde as peças aliadas poderá se mexer
        checks = []  # local onde está a peça inimiga ameaçando o check
        inCheck = False

        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()  # reseta pinos possíveis
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != "K":
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break

                    if endPiece[0] == enemyColor:
                        type = endPiece[1]
                        # Possibilidades dessas condições complexas
                        # 1) ortogonal para o rei e para o torre
                        # 2) diagonal para o rei e para o bispo
                        # 3) 1 casa para o rei e para o pino
                        # 4) todas as direções para a rainha
                        # 5) todas as direções caso a peça seja o outro rei

                        if (0 <= j <= 3 and type == 'R') or (4 <= j <= 7 and type == 'B') or (i == 1 and type == 'P' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or (type == "Q" or (i == 1 and type == "K")):
                            if possiblePin == ():  # Nenhuma peça para possível bloqueio, então é check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:  # Peça inimiga não fez o check
                            break
                else:
                    break  # retirando a tábua

        # verificando se há um possível check do cavalo
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2),
                       (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                # Cavalo inimigo atacando o rei
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))

        return inCheck, pins, checks

    '''
    obtendo todos os movimentos das peças, sua linha e coluna e adicionando esse movimento na lista
    '''

    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()

        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:  # Movimento peça branca
            if self.board[r-1][c] == "--":
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r, c), (r-1, c), self.board))
                    if r == 6 and self.board[r-2][c] == "--":
                        moves.append(Move((r, c), (r-2, c), self.board))

            # captura
            if c-1 >= 0:  # captura para esqueda
                if self.board[r-1][c-1][0] == 'b':
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((r, c), (r-1, c-1),  self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b':
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((r, c), (r-1, c+1),  self.board))

        else:  # movimento peça preta
            if self.board[r+1][c] == '--':
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((r, c), (r+1, c), self.board))
                    if r == 1 and self.board[r+2][c] == "--":
                        moves.append(Move((r, c), (r+2, c), self.board))

            # captura
            if c-1 >= 0:  # captura para esqueda
                if self.board[r+1][c-1][0] == 'w':
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((r, c), (r+1, c-1), self.board))

            if c+1 <= 7:  # Captura para direita
                if self.board[r+1][c+1][0] == 'w':
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((r, c), (r+1, c+1), self.board))

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()

        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                # Retirando essa tratativa caso a peça seja a rainha
                if self.board[r][c][1] != "Q":
                    self.pins.remove(self.pins[i])
                break

        # cima baixo direita e esquerda
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # Na tábua
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":  # Espaço vazio válido
                            moves.append(
                                Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(
                                Move((r, c), (endRow, endCol), self.board))
                            break
                        else:  # peça amiga invalida
                            break
                else:  # movimento fora da tábua
                    break

    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()

        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        # Diagonais
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # Na tábua
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":  # Espaço vazio válido
                            moves.append(
                                Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(
                                Move((r, c), (endRow, endCol), self.board))
                            break
                        else:  # peça amiga invalida
                            break
                else:  # movimento fora da tábua
                    break

    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2),
                       (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    # Não for um aliado (casa vazia ou peça inimiga)
                    if endPiece[0] != allyColor:
                        moves.append(
                            Move((r, c), (endRow, endCol), self.board))

    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)

        allyColor = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                # Não for um aliado (casa vazia ou peça inimiga)
                if endPiece[0] != allyColor:
                    if allyColor == "w":
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checksForPinsAndChecks()
                    if not inCheck:
                        moves.append(
                            Move((r, c), (endRow, endCol), self.board))
                    if allyColor == "w":
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)

    def getCastleMoves(self, r, c, moves):
        pass

    def getKingsideCastleMoves(self, r, c, moves):
        pass

    def getQueensideCastleMoves(self, r, c, moves):
        pass


class Move():
    # Numerando as linhas e colunas de 1 a 8
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    # Mapeando as colunas de A a H
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
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
        self.moveID = self.startRow * 1000 + self.startCol * \
            100 + self.endRow * 10 + self.endCol
        print(self.moveID)
        self.isPawnPromotion = False
        if (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7):
            self.isPawnPromotion = True

    # igualdade do objeto da class move

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID

    # Essa função retorna a posição da casa e da coluna
    def getChessNot(self):
        return f"{self.getRankFile(self.startRow, self.startCol)} -- {self.getRankFile(self.endRow, self.endCol)}"

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
