# # 14 Tic-Tac-Toe Checker

# def is_solved(board):
#     main_diag = [board[i][i] for i in range(len(board))]
#     if (main_diag.count(main_diag[0]) == len(main_diag)) and (main_diag[0] ==1 or main_diag[0] ==2):
#         return main_diag[0]
#     n = len(board)
#     sec_diag = [board[i][n-1-i] for i in range(n)]
#     if (sec_diag.count(sec_diag[0]) == len(sec_diag)) and (sec_diag[0] ==1 or sec_diag[0] == 2):
#         return sec_diag[0]
#     for row in board:
#         if row[0] != 0 and all(elem == row[0] for elem in row):
#             return row[0]
        
#     for i in range(len(board)):
#         if board[0][i] != 0 and all(board[r][i] == board[0][i] for r in range(len(board))):
#             return board[0][i]
#     if not any(0 in row for row in board):
#         return 0
    
#     return -1
# print(is_solved([[2, 1, 1],
#                  [2, 2, 2],
#                  [1, 0, 1]]))

def is_solved(board):
    n = len(board)

    main_diag = [board[i][i] for i in range(n)]
    if main_diag[0] != 0 and all(x == main_diag[0] for x in main_diag):
        return main_diag[0]

    sec_diag = [board[i][n-1-i] for i in range(n)]
    if sec_diag[0] != 0 and all(x == sec_diag[0] for x in sec_diag):
        return sec_diag[0]

    for row in board:
        if row[0] != 0 and all(x == row[0] for x in row):
            return row[0]

    for i in range(n):
        if board[0][i] != 0 and all(board[r][i] == board[0][i] for r in range(n)):
            return board[0][i]

    return -1 if any(0 in row for row in board) else 0