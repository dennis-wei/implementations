MERSENNE_EXPONENTS = [7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279]
pow_arr = [128]

def get_larger_prime(n):
    largest_prime = 0
    for i, ex in enumerate(MERSENNE_EXPONENTS[1:], start=1):
        mersenne = pow_arr[-1] - 1
        if n < mersenne:
            return mersenne
        prev_ex = MERSENNE_EXPONENTS[i-1]
        prev_pow = pow_arr[i-1]
        pow_arr.append(prev_pow * pow(2, ex - prev_ex))
