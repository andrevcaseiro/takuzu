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
    compare_searchers
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
        self.rowCounts[key[0]][2] -= 1
        self.rowCounts[key[0]][item] += 1
        self.colCounts[key[1]][2] -= 1
        self.colCounts[key[1]][item] += 1

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        value = self.lines[
            row, col] if 0 <= row < self.n and 0 <= col < self.n else None

        return value

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        upper = self.lines[row - 1, col] if row - 1 >= 0 else None
        lower = self.lines[row + 1, col] if row + 1 < self.n else None

        return (lower, upper)

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        upper = self.lines[row, col - 1] if col - 1 >= 0 else None
        lower = self.lines[row, col + 1] if col + 1 < self.n else None

        return (upper, lower)

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board."""

        def counts(arr):
            unique, counts = np.unique(arr, return_counts=True)
            c = dict(zip(unique, counts))

            if 0 not in c:
                c[0] = 0
            if 1 not in c:
                c[1] = 0
            if 2 not in c:
                c[2] = 0

            return c

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
        board.rowCounts = [counts(board.lines[i, :]) for i in range(board.n)]
        board.colCounts = [counts(board.lines[:, i]) for i in range(board.n)]

        board.goalCounts = ((board.n-1)/2, (board.n+1) /
                            2) if board.n % 2 != 0 else (board.n/2, board.n/2)

        return board

    def copy(self):
        """Retorna uma cópia do tabuleiro"""
        board = Board()

        board.n = self.n
        board.lines = np.copy(self.lines)
        board.globCounts = self.globCounts.copy()
        board.rowCounts = [counts.copy() for counts in self.rowCounts]
        board.colCounts = [counts.copy() for counts in self.colCounts]
        board.goalCounts = self.goalCounts

        return board

    # TODO: outros metodos da classe


class Takuzu(Problem):

    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = TakuzuState(board)

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        final_res = []

        for i in range(state.board.n):
            for j in range(state.board.n):

                if state.board[i, j] == 2:

                    res = []

                    adj_row = state.board.adjacent_horizontal_numbers(i, j)
                    adj_col = state.board.adjacent_vertical_numbers(i, j)

                    if not (1 == adj_row[0] == adj_row[1]
                            or 1 == adj_col[0] == adj_col[1]
                            or 1 == adj_row[0] == state.board.get_number(i, j - 2)
                            or 1 == adj_row[1] == state.board.get_number(i, j + 2)
                            or 1 == adj_col[0] == state.board.get_number(i + 2, j)
                            or 1 == adj_col[1] == state.board.get_number(i - 2, j)
                            or state.board.rowCounts[i][1] == state.board.goalCounts[1]
                            or state.board.colCounts[j][1] == state.board.goalCounts[1]):
                        res.append((i, j, 1))
                    if not (0 == adj_row[0] == adj_row[1]
                            or 0 == adj_col[0] == adj_col[1]
                            or 0 == adj_row[0] == state.board.get_number(i, j - 2)
                            or 0 == adj_row[1] == state.board.get_number(i, j + 2)
                            or 0 == adj_col[0] == state.board.get_number(i + 2, j)
                            or 0 == adj_col[1] == state.board.get_number(i - 2, j)
                            or state.board.rowCounts[i][0] == state.board.goalCounts[1]
                            or state.board.colCounts[j][0] == state.board.goalCounts[1]):
                        res.append((i, j, 0))
                    if len(res) <= 1:
                        return res
                    if not final_res:
                        final_res = res

        return final_res

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        newBoard = state.board.copy()
        newBoard[action[0], action[1]] = action[2]

        return TakuzuState(newBoard)

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""

        # tabuleiro preenchido
        if state.board.globCounts[2] != 0:
            return False

        # numero igual de 0 e 1 em cada linha e coluna
        for i in range(state.board.n):
            if (state.board.rowCounts[i][0] not in state.board.goalCounts
                    or state.board.colCounts[i][0] not in state.board.goalCounts):
                return False

        # linhas e colunas diferentes
        for i in range(state.board.n):
            temp_row = state.board.lines[i]
            temp_col = state.board.lines[:, i]
            for j in range(i + 1, state.board.n):
                if np.array_equal(temp_col,
                                  state.board.lines[:, j]) or np.array_equal(
                                      temp_row, state.board.lines[j]):
                    return False

        # nao ha mais que 2 adjacentes
        for i in range(state.board.n):
            for j in range(1, state.board.n - 1):
                adj_row = state.board.adjacent_horizontal_numbers(i, j)
                adj_col = state.board.adjacent_vertical_numbers(j, i)
                num_row = state.board.get_number(i, j)
                num_col = state.board.get_number(j, i)
                if (num_row == adj_row[0] == adj_row[1]
                        or num_col == adj_col[0] == adj_col[1]):
                    return False

        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""

        row_h = 0
        col_h = 0

        for i in range(node.state.board.n):
            row_h += node.state.board.goalCounts[1] - max(node.state.board.rowCounts[i][0], node.state.board.rowCounts[i][1])
            col_h += node.state.board.goalCounts[1] - max(node.state.board.colCounts[i][0], node.state.board.colCounts[i][1])
        
        return max(row_h, col_h)

    # TODO: outros metodos da classe

class Takuzu2(Takuzu):
    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        
        row_h = 0
        col_h = 0

        for i in range(node.state.board.n):
            row_h += 2*node.state.board.n - 2*min(node.state.board.rowCounts[i][0], node.state.board.rowCounts[i][1])
            col_h += 2*node.state.board.n - 2*min(node.state.board.colCounts[i][0], node.state.board.colCounts[i][1])
        
        return max(row_h, col_h)

class Takuzu3(Takuzu):
    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        
        row_h = 0
        col_h = 0

        for i in range(node.state.board.n):
            row_h += 2*node.state.board.n - 2*min(node.state.board.rowCounts[i][0], node.state.board.rowCounts[i][1])
            col_h += 2*node.state.board.n - 2*min(node.state.board.colCounts[i][0], node.state.board.colCounts[i][1])
        
        return min(row_h, col_h)

if __name__ == "__main__":
    board = Board.parse_instance_from_stdin()
    problem = Takuzu(board)

    goal_node = breadth_first_tree_search(problem)

    print(goal_node.state.board, end="")
