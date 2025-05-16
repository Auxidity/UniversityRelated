
def permutations(s):
    if len(s) == 0:
        return ['']
    
    perms = []
    for i in range(len(s)):
        first_char = s[i]
        remaining_chars = s[:i] + s[i+1:]
        for perm in permutations(remaining_chars):
            perms.append(first_char + perm)
    
    return perms

# Example usage
input_set = "abc"
result = permutations(input_set)
print(result)