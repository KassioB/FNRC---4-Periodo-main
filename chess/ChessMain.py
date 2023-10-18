import ChessEngine
import pygame as p
import math


width = height = 500
dim = 8 #Dimensions (8x8)
sqsize = height // dim
maxfps = 20
images = {} 

def loadImages():
    pieces = ["wP","wR","wN","wB","wQ","wK","bP","bR","bN","bB","bQ","bK"]
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("images/" + piece +".png"),(sqsize,sqsize))
        
def main():
    p.init()
    screen = p.display.set_mode((width,height))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))
    gameOver= False
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # flag variavel para quando um movimento é feito
    loadImages() # As imagens é chamada apenas uma vez antes do loop
    running = True
    animate = False # flag para animação
    sqSelected = () # Armazena a casa que o usuário clicar, (Tupla: (linha, coluna))
    playerClicks = [] # mantem armazenado os clicks do usuário (duas tulplas: [(6,4),(4,4)])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                
            elif e.type == p.MOUSEBUTTONDOWN : # Evento de click do mouse
                if not gameOver:
                    location = p.mouse.get_pos() # captura a posição do mouse
                    col = location[0]//sqsize
                    row = location[1]//sqsize
                    if sqSelected == (row,col): # o usuário clickou nas mesmas casas
                        sqSelected = ()
                        playerClicks = [] # retira o click do player
                    else:
                        sqSelected = (row,col)
                        # Adicionando o primeiro e segundo click do usuário
                        playerClicks.append(sqSelected)

                    if len(playerClicks) == 2: # depois do segundo click
                        move = ChessEngine.Move(
                          playerClicks[0],playerClicks[1], gs.board)
                      
                        if move in validMoves: # verificação de movimentos validos
                          gs.makeMove(move)
                          moveMade = True
                          animate = True
                          sqSelected = ()  # reseta a seleção
                          playerClicks = []  # resetando os clicks
                              
                        if not moveMade:
                            playerClicks = [sqSelected]
            
                    
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #volta a jogada pressionando 'z'
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r: #reseta o jogo pressionando 'r'
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False

                    
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'O PRETO VENCEU POR CHECKMATE')
            else:
                drawText(screen, 'O BRANCO VENCEU POR CHECKMATE')
        elif gs.stalemate:
            gameOver = True
            drawText(screen, 'stalemate')

        clock.tick(maxfps)
        p.display.flip()




def highlightSquares(screen, gs, validMoves, sqSelected): # mostra os movimentos possiveis
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((sqsize, sqsize))
            s.set_alpha(100)
            s.fill(p.Color('dark gray'))
            screen.blit(s, (c*sqsize, r*sqsize))
            s.fill(p.Color('blue'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*sqsize, move.endRow*sqsize))

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves,sqSelected)
    drawPieces(screen, gs.board)

def drawBoard(screen):# desenha o tabuleiro
    global colours
    colours = [p.Color("white"),p.Color("black")]
    for r in range(dim):
        for c in range(dim):
            colour = colours[((r + c) % 2)]
            p.draw.rect(screen, colour, p.Rect(c*sqsize, r*sqsize, sqsize, sqsize))
            
            

def drawPieces(screen,board):# desenha as peças no tabuleiro
    for r in range(dim):
        for c in range(dim):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c*sqsize, r*sqsize, sqsize, sqsize))

def animateMove(move,screen, board, clock): #animação da peça
    global colours
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 7
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = ((move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount))
        drawBoard(screen)
        drawPieces(screen, board)
        colour = colours [(move.endRow + move.endCol) % 2]
        endSquare = p.Rect (move.endCol*sqsize, move.endRow*sqsize, sqsize, sqsize)
        p.draw.rect(screen, colour, endSquare)
        if move.pieceCaptured != '--':
            screen.blit(images[move.pieceCaptured], endSquare)
        screen.blit(images[move.pieceMoved], p.Rect(c*sqsize,r*sqsize,sqsize,sqsize))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text): # tela de gameover
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, width, height).move(width/2 - textObject.get_width()/2, height/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("blue"))
    screen.blit(textObject, textLocation.move(2, 2))

if __name__ == "__main__":
    main()