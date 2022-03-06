import chess
from calendar import c
from cgi import print_form
import os
from random import randint

ultimoMov = None
# Heurística - Atribuindo valores as posições do tabuleiro.
# Cada peça no tabuleiro, dependendo de sua posição, vai possuir valores maiores se favorável ou menores se desfavorável.
# Por exemplo a peça Rei, ao passar do centro suas chances serão muito menores, logo valores menores, pois está em uma posição desfavoráveis, que resultara em valores negativos.
peaoBranco = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

# Transforma os valores para as peças pretas, o oposto
peaoPreto = peaoBranco[::-1]

cavaloBranco = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

cavaloPreto = cavaloBranco[::-1]

bispoBranco = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

bispoPreto = bispoBranco[::-1]

torreBranco = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]

torrePreto = torreBranco[::-1]

rainhaBranco = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

rainhaPreto = rainhaBranco[::-1]

reiBranco = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]

reiPreto = reiBranco[::-1]

# Algoritmo Minmax
def minimaxRoot(depth,board,isMaximizing):
    legalMoves = board.legal_moves
    bestMove = -9999
    finalMove = None
    for x in legalMoves:
        move = chess.Move.from_uci(str(x))
        board.push(move)
        value = max(bestMove, minimax(depth - 1, board,-10000,10000, not isMaximizing))
        board.pop()
        if value > bestMove:
            bestMove = value
            finalMove = move
    return finalMove

# Algoritmo Minmax
def minimax(depth, board, alpha, beta, maximizing):
    if(depth == 0):
        return -evaluateBoard(board)
    legalMoves = board.legal_moves
    if(maximizing):
        bestMove = -9999
        for x in legalMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            bestMove = max(bestMove,minimax(depth - 1, board,alpha,beta, not maximizing))
            board.pop()
            alpha = max(alpha,bestMove)
            if beta <= alpha:
                return bestMove
        return bestMove
    else:
        bestMove = 9999
        for x in legalMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            bestMove = min(bestMove, minimax(depth - 1, board,alpha,beta, not maximizing))
            board.pop()
            beta = min(beta,bestMove)
            if beta <= alpha:
                return bestMove
        return bestMove



# Algoritmo que avalia o tabuleiro
# ?
def evaluateBoard(board):
    i = 0
    evaluation = 0
    x = board.turn
    while i < 63:
        i += 1
        evaluation = evaluation + (getPieceValue(str(board.piece_at(i)),i) if x else -getPieceValue(str(board.piece_at(i)),i))
    return evaluation

  
# Algoritmo que atribui valor a peça
# Cada peça tem seu valor, sendo uns maiores que os outros (K(King) > P(Pawn))
# Parâmetros da funçao são: peça e sua posição no tabuleiro
def getPieceValue(piece, i):
    # Se a peça for nula, retorno 0 e não atribuo nenhum valor pra ela
    if(piece == None):
        return 0
    value = 0
    # Exemplo P, Pawn, Peão
    # Se a peça for um peão, eu dou o valor 10 pra ela, e somo com o valor da sua posição atual  no tabuleiro, de acordo com a heurística, onde cada peça, dependendo de sua posição no tabuleiro, pode assumir valores diferentes.
    if piece == "P" or piece == "p":
        value = 10 + ((peaoBranco[i]) if piece == "P" else (peaoPreto[i]))
    if piece == "N" or piece == "n":
        value = 30 + ((cavaloBranco[i]) if piece == "N" else (cavaloPreto[i]))
    if piece == "B" or piece == "b":
        value = 30 + ((bispoBranco[i]) if piece == "B" else (bispoPreto[i]))
    if piece == "R" or piece == "r":
        value = 50 + ((torreBranco[i]) if piece == "R" else (torrePreto[i]))
    if piece == "Q" or piece == "q":
        value = 90 + ((rainhaBranco[i]) if piece == "Q" else (rainhaPreto[i]))
    if piece == 'K' or piece == 'k':
        value = 900 + ((reiBranco[i]) if piece == "K" else (reiPreto[i]))
    return value



def VezUsuario():
  print("Vez do Jogador!")
  # Mostra as possíveis jogadas
  print("Essas são suas possíveis jogadas: ")
  print("=====================================================================")
  print(list(board.legal_moves))
  print("=====================================================================")
  
  # Faz o movimento de acordo com o input do jogador
  movimento = chess.Move.from_uci(input("Qual o seu movimento? "))
  board.push(movimento)

def VezIA():
  print("Vez da IA!")
      # Movimento de acordo com o algoritmo Minmax
  move = minimaxRoot(4,board,True)
  move = chess.Move.from_uci(str(move))
  # Função que faz o movimento
  print('A IA fez a seguinte jogada: >>{}<<'.format(move))
  board.push(move)

  
# Função para ver de quem é a vez
# Se N = 0, é o programa
# Se N = 1, é o usuário
def turno(rodada): 
    n = rodada % 2
    if n == 0:
      return 0
    else:
      return 1



# Sorteia 0 ou 1 pra decidir quem irá começar a partida
rodada = randint(0,1)
board = chess.Board()

print("                           Bem vindo(a)!")
print("                  ♕  EP 1 - Engine de Xadrez  ♕")
print("\n")
aux = 0
while aux != "sim":
  aux = input("Deseja iniciar a partida? (sim ou nao) \n").lower()
  if( aux == "nao"):
    print("Ok! :( ")

print("Ok, iremos sortear quem começa.")
if (rodada == 1):
  print("Jogador foi sorteado!")
else:
  print("IA foi sorteada!")

print("\n")

#corJogador = int((input("Por favor, escolha sua cor (0 = Branco), (1 = Preto): ")))

# Condição pra iniciar o jogo
if aux == 'sim':
  # Loop da partida
  # Enquanto não é checkmate ou empate, o jogo continua
  while board.is_checkmate() == False or board.is_stalemate() == False:
    # Se a vez é do jogador
    #if board.turn == corJogador:
    if turno(rodada) == 1:
      VezUsuario()
    # Se a vez for da IA
    else:
      VezIA()

    ultimoMov = turno(rodada)
    rodada = rodada + 1 
    print(board)
    
  print("=======================================================================")
  if(ultimoMov == 0):
    print("Vitória da IA!")
  else:
    print("Vitória do Usuário")
# retorno do move = 
#PIECE_NAME = {'p': 'Pawn', 'b': 'Bishop', 'n': 'Knight', 'r': 'Rook', 'q': 'Queen', 'k': 'King'}
#print(PIECE_NAME.values())