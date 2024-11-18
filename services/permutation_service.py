import random
from math import factorial


def random_permutation(n):
    used_indices = set()
    for _ in range(n):
        while True:
            rand_index = random.randint(1, n)
            if rand_index not in used_indices:
                used_indices.add(rand_index)
                yield rand_index
                break

def kth_permutation_fast(elements, k):
    n = len(elements)
    k %= factorial(n)
    factorials = [factorial(i) for i in range(n)]
    # elements = sorted(elements)
    used = [False] * n
    permutation = []

    for i in range(n):
        fact = factorials[n - 1 - i]
        index = k // fact
        k %= fact
        
        count = -1
        for j in range(n):
            if not used[j]:
                count += 1
            if count == index:
                permutation.append(elements[j])
                used[j] = True
                break

    return permutation
