# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 96:
# 99180 Andre Valente Caseiro
# 99257 Joao Vieira Antunes

from hashlib import new
import sys
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    def __repr__(self) -> str:
        out = ""
        for i in range(self.n):
            for j in range(self.n):
                if j != 0:
                    out += "\t"
                out += str(self.lines[i, j])
            out += "\n"
        return out

    def __len__(self):
        return self.n
    
    def __getitem__(self, key):
        return self.lines[key]
    
    def __setitem__(self, key, item):
        self.lines[key] = item
        self.globCounts[2] -= 1
        self.globCounts[item] += 1
        self.rowCounts[key[0]][2] -=1
        self.rowCounts[key[0]][item] +=1
        self.colCounts[key[1]][2] -=1
        self.colCounts[key[1]][item] += 1

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        value = self.lines[row, col]

        return value

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        upper = self.lines[row-1, col] if row-1 > 0 else None
        lower = self.lines[row+1, col] if row+1 < self.n else None

        return (lower, upper)

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        upper = self.lines[row, col-1] if col-1 > 0 else None
        lower = self.lines[row, col+1] if col+1 < self.n else None

        return (upper, lower)

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board."""

        def counts(arr):
            unique, counts = np.unique(arr, return_counts=True)
            return dict(zip(unique, counts))

        # TODO        
        board = Board()

        board.n = int(sys.stdin.readline())
        lines = []

        for i in range(board.n):
            input = sys.stdin.readline()
            line = input.split("\t")
            line_int = [int(item) for item in line]
            lines.append(line_int)
        
        board.lines = np.array(lines)

        board.globCounts = counts(board.lines)
        board.rowCounts = [counts(board.lines[i,:]) for i in range(board.n)]
        board.colCounts = [counts(board.lines[:,i]) for i in range(board.n)]

        return board
    
    def copy(self):
        """Retorna uma cópia do tabuleiro"""
        board = Board()

        board.n = self.n
        board.lines = np.copy(self.lines)
        board.globCounts = self.globCounts.copy()
        board.rowCounts = self.rowCounts.copy()
        board.colCounts = self.colCounts.copy()

        return board

    # TODO: outros metodos da classe


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.board = board
        self.initial = TakuzuState(board)

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        res = []

        for i in range(self.board.n):
            for j in range(self.board.n):
                if self.board.lines[i, j] == 2:
                    res.append((i, j, 0))
                    res.append((i, j, 1))
        
        return res

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        newBoard = state.board.copy()
        newBoard.lines[action[0], action[1]] = action[2]

        return TakuzuState(newBoard)

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        # TODO

        #tabuleiro preenchido
        if self.board.globCounts[2] != 0:
            return False

        #numero igual de 0 e 1 em cada linha e coluna
        for i in range(self.board.n):
            ul = self.board.lines[i].count(1)
            zl = self.board.lines[i].count(0)
            uc = self.board.lines[:,i].count(1)
            zc = self.board.lines[:,i].count(0)
            if ul != zl or uc != zc:
                return False                
        
        #linhas e colunas diferentes
        for i in range(self.board.n):
            temp_row = self.board.lines[i]
            temp_col = self.board.lines[:,i]
            for j in range(i+1, self.board.n):
                if np.array_equal(temp_col,self.board.lines[:,j]) or np.array_equal(temp_row,self.board.lines[j]):
                    return False 

        #nao ha mais que 2 adjacentes
        for i in range(self.board.n):
            for j in range(1,self.board.n-1):
                adj_row = self.board.adjacent_horizontal_numbers(i, j)
                adj_col = self.board.adjacent_vertical_numbers(j, i)
                num_row = self.board.get_number(i,j)
                num_col = self.board.get_number(j,i)
                if num_row == adj_row[0] and num_row == adj_row[1] or num_col == adj_col[0] and num_col == adj_col[1]:
                    return False

        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


#if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    #board = Board.parse_instance_from_stdin()
    #problem = Takuzu(board)
#
    ## Obter o nó solução usando a procura em profundidade:
    #goal_node = depth_first_tree_search(problem)
    ## Verificar se foi atingida a solução
    #print("Is goal?", problem.goal_test(goal_node.state))
    #print("Solution:\n", goal_node.state.board, sep="")
