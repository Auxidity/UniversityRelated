#Task 1

Arr = [10, 20, 30, 40]

n = len(Arr)
k = 5

def maximumSumSubarray(arr, n, k):
    if k > n:
        return "There needs to be more or equal amount of  array objects than what are being summed together"

    maxSum = -10**9 #for handling negative array numbers
    currentSum = 0


    for i in range(k):
        currentSum += arr[i]

    maxSum = max(maxSum, currentSum)

    for i in range (k, n):
        currentSum += arr[i] - arr[i-k]
        maxSum = max(maxSum, currentSum)
    
    return maxSum

#a = maximumSumSubarray(Arr, n, k)
#print(a)

#Task 2

def downwardDiagonal(matrix, n):
    anti_diagonals = []

    # Iterate over columns
    for j in range(n):
        row = 0
        col = j
        anti_diagonal = []

        # Traverse along the current anti-diagonal
        while col >= 0:
            anti_diagonal.append(matrix[row][col])
            row += 1
            col -= 1

        anti_diagonals.append(anti_diagonal)

    # Iterate over rows excluding the main diagonal
    for i in range(1, n):
        row = i
        col = n - 1
        anti_diagonal = []

        # Traverse along the current anti-diagonal
        while row < n:
            anti_diagonal.append(matrix[row][col])
            row += 1
            col -= 1

        anti_diagonals.append(anti_diagonal)

    return anti_diagonals

'''# Example usage:
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
n = len(matrix)
anti_diagonals = downwardDiagonal(matrix, n)
for anti_diagonal in anti_diagonals:
    print(anti_diagonal, end=", ")
print()
'''

#Task 3


n = 17 #Foreign
m = 17 #Indian

def rooms(n, m): #n = foreign, m = indian
    k = min(n,m)
    while k > 1:
        if n % k == 0 and m % k == 0:
            break
        k -= 1
    foreign = n // k if n % k == 0 else n // k + 1 #Floor division and check with modulo if leftover
    indian = m // k if m % k == 0 else m // k + 1
    total = foreign + indian
    return total

#min_rooms = rooms(n, m)
#print(min_rooms)

#Task 4

def countFriendsPairings(n):
    if n < 1:
        return "cannot count pairs with 0 or negative people"
    if n == 1:
        return 1 #No pairings possible, so only 1 single
    
    # Initialize DP table
    dp = [0] * (n + 1)
    dp[0] = dp[1] = 1 #Initializing base cases
    
    # Fill DP table using recurrence relation. dp[i-1] represents the ways to form pairs if i-1 is unpaired
    # (i-1) represents the number of choices for pairs (i-1)th person has
    # dp(i-2) then represents the remaining number of ways to form pairs after initial pair has been made
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + (i - 1) * dp[i - 2]
    
    return dp[n]

# Example usage:
#n = 4
#print("Total possible pairings:", countFriendsPairings(n))

#Task 5

def productOfPairs(n, arr):
    array_sum = 0
    
    for i in range(n-1): #Not absolutely certain why this works with n-1 and n, it should give index error when i = n due to j = i+1 if range is i to n
        for j in range(i+1, n):
            array_sum += arr[i] * arr[j]
    return array_sum % (10**9 + 7)

    

arr = [2,2,3,7,5,2,2,162626,2626346]
n = len(arr)
x = productOfPairs(n, arr)
print(x)