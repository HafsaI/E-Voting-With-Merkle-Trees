import hashlib, random, csv


def gcd(a, b) -> int:
    """
    Calculates the Greatest common denominator of two integers.

    Args:
    - a: any integer
    - b: any integer

    Returns:
    the calculated gcd value of the numbers.

    """
    while a != 0:
        a, b = b % a, a
    return b


def findModInverse(a, m) -> int:
    """
    Finds the modular inverse of two integers.

    Args:
    - a: any integer
    - m: any integer

    Returns:
    The modular inverse of the two integers

    """
    if gcd(a, m) != 1:
        return None

    m0, y, x = m, 0, 1

    if m == 1:
        return 0

    while a > 1:
        q = a // m
        t = m

        m = a % m
        a = t
        t = y

        y = x - q * y
        x = t

    if x < 0:
        x = x + m0

    return x


def MillerRabin(num) -> bool:
    """
    Checks if num is prime or not using probabilistic method.

    Args:
    - num: any number

    Returns:
    True if number is prime.
    False if not.

    """
    s = num - 1
    t = 0

    while s % 2 == 0:
        s = s // 2
        t += 1
    for _ in range(5):
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v == 1 or v == num - 1:
            continue
        for _ in range(t - 1):
            v = pow(v, 2, num)
            if v == num - 1:
                break
        else:
            return False
    return True


def isHighPrime(num) -> bool:
    """
    Checks if number is prime or not,
    and makes sure it is a big prime,
    since RSA requires big prime.

    Args:
    - num: any integer

    Returns:
    True is number is Prime. False if it is not.

    """
    if num < 2:
        return False
    lowPrimes = getLowPrimes(1000)

    if num in lowPrimes:
        return True
    for prime in lowPrimes:
        if num % prime == 0:
            return False
    return MillerRabin(num)


def getLowPrimes(num) -> list:
    """
    Generates a list of all prime numbers lower than 'num'

    Args:
    - num: any integer

    Returns:
    list of all primes lower than num.

    """
    n = set(range(num, 1, -1))
    lowPrimes = []
    while n:
        p = n.pop()
        lowPrimes.append(p)
        n.difference_update(set(range(p * 2, num + 1, p)))
    return lowPrimes


def generatePrime(keysize) -> int:
    """
    Generates a random Prime number using given keysize.

    Args:
    - keysize

    Returns:
    randomly generated prime number.

    """
    while True:
        num = random.randrange(2 ** (keysize - 1), 2 ** (keysize))
        if isHighPrime(num):
            return num


def generateKey(keySize) -> tuple:
    """
    Generates Public and Private key using RSA Encryption method.
    The method used was followed from this article:
    https://core.ac.uk/download/pdf/11779635.pdf

    Args:
    - keysize: Can be set according to the user,
    the greater the keysize the more greater the
    public and private keys and the more secure the
    encryption.

    Returns:
    a tuple of (publicKey, privateKey)

    """

    p = generatePrime(keySize)
    q = generatePrime(keySize)
    n = p * q
    phi = (p - 1) * (q - 1)

    while True:
        e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
        if gcd(e, phi) == 1:
            break

    d = findModInverse(e, phi)
    publicKey = (str(n), str(e))
    privateKey = (str(n), str(d))
    return (publicKey, privateKey)


def storeData(reg_data) -> None:
    """
    Stores Hashed VoterData and public and private key.

    Args:
    - reg_data: lst consisting name + id + year + hashed vid

    Returns:
    none
    """
    v = reg_data[0] + reg_data[1] + reg_data[2]
    vid = reg_data[3]
    vdata = hashlib.shake_256(v.encode("utf-8")).hexdigest(5)
    publicKey, privateKey = generateKey(1024)
    with open("Files\\voters_data.csv", "a", newline="") as csvfile:
        file = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        file.writerow(
            [
                vid,
                vdata,
                publicKey[0] + "," + publicKey[1],
                privateKey[0] + "," + privateKey[1],
            ]
        )