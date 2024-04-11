# Function to find whether a number is prime or not

def is_prime(n: int) -> bool:   # Defining datatype of arguments and return type
    if n<2: return 0
    num = 2
    while num*num <= n:
        isprime = False if n % m == 0 else True