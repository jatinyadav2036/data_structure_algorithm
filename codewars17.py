# Determinant of Matrix

def determinant(matrix):
    n = len(matrix)

    # Base case: 1x1 matrix
    if n == 1:
        return matrix[0][0]

    # Base case: 2x2 matrix
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0

    # Expansion along the first row
    for col in range(n):
        # Create minor matrix
        minor = [
            row[:col] + row[col + 1:]
            for row in matrix[1:]
        ]

        # Cofactor expansion
        det += ((-1) ** col) * matrix[0][col] * determinant(minor)

    return det

# import numpy as np

# def determinant(a):
#     return round(np.linalg.det(np.matrix(a)))