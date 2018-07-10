from foal.dynamic_programming import memoize


@memoize()
def binomial_coeff(n, k):
    if (k == 0 or n == k):
        return 1
    else:
        return binomial_coeff(n - 1, k - 1) + binomial_coeff(n - 1, k)
