import math
import random

def generate_large_prime(bits=50):
    """
    Generates a large prime number of specified bits.
    """
    prime_candidate = random.getrandbits(bits)
    while not is_prime(prime_candidate):
        prime_candidate += 1
    return prime_candidate

def is_prime(number):
    """
    Checks if a number is prime.
    """
    if number % 2 == 0 and number > 2:
        return False
    return all(number % i != 0 for i in range(3, int(math.sqrt(number)) + 1, 2))

def find_primitive_root(modulus):
    """
    Finds a primitive root for a given prime modulus.
    """
    phi = modulus - 1  # Euler's Totient Function
    prime_factors = find_prime_factors(phi)

    for potential_root in range(2, modulus):
        if all(pow(potential_root, phi // factor, modulus) != 1 for factor in prime_factors):
            return potential_root
    return None

def find_prime_factors(number):
    """
    Finds all prime factors of a given number.
    """
    factors = []
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            factors.append(divisor)
            while number % divisor == 0:
                number //= divisor
        divisor += 1
    if number > 1:
        factors.append(number)
    return factors

def compute_shared_key(private_key, modulus, base):
    """
    Computes the public key.
    """
    return pow(base, private_key, modulus)

def generate_random_private_key(modulus):
    """
    Generates a random private key.
    """
    return random.randint(1, modulus - 1)

prime = generate_large_prime()
g = find_primitive_root(prime)
def exchange_keys(participants):
    """
    Simulates key exchange between participants.
    """
    # Phase 1: Generate and share public keys
    for i in range(len(participants)):
        participants[(i + 1) % len(participants)].shared_key = compute_shared_key(
            participants[i].private_key, prime, g)

    # Phase 2: Generate intermediate keys based on received public keys
    for i in range(len(participants)):
        participants[(i + 1) % len(participants)].intermediate_key = compute_shared_key(
            participants[i].private_key, prime, participants[i].shared_key)

    # Finalize mutual keys based on intermediate keys
    for participant in participants:
        participant.finalize_mutual_key()
