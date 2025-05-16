
def add_column(matrix):


    for row in matrix:
        row.append(sum(row))
    return matrix


matrix = [
    [11,3], 
    [3,4]
]

new_matrix = add_column(matrix)

for row in new_matrix:
    print(row)