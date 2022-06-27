from takuzu import Takuzu, Board
from search import astar_search, breadth_first_tree_search, compare_searchers, depth_first_tree_search, greedy_search

board = Board.parse_instance_from_stdin()

compare_searchers(problems=[Takuzu(board)],
                  header=['Searcher', 'Takuzu2', 'Takuzu3'],
                  searchers=[astar_search,
                             breadth_first_tree_search,
                             depth_first_tree_search,
                             greedy_search])
