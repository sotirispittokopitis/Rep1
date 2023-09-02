import hashlib
import json
import random
# The following code is taken from:
# https://www.geeksforgeeks.org/blockchain-elliptic-curve-digital-signature-algorithm-ecdsa/
# Although some formulas/parts remain the same, some alterations are added to simulate the XRPL
# ----------------------------------------------------------------
p = pow(2, 255) - 19
base = 15112221349535400772501151409588531511454012693041857206046113283949847762202, 46316835694926478169428394003475163141307993866256225615783033603165251855960
# ----------------------------------------------------------------
def findPositiveModulus(a, p):
    if a < 0:
        part1 = p * int(abs(a) / p)
        a = a + part1 + p
    return a % p
# ----------------------------------------------------------------
def textToInt(text):
    encoded_text = text.encode()
    hex_text = encoded_text.hex()
    int_text = int(hex_text, 16)
    return int_text
# ----------------------------------------------------------------
# Function to find greatest
# common divisor(gcd) of a and b
def gcd(a, b):
    while a != 0:
        value1 = a
        value2 = b
        theRemainder = value2 % value1
        a = theRemainder
        b = value1
    return b
# ----------------------------------------------------------------
# Function to find the modular inverse
# of a mod m
def findModInverse(a, m):
    if a < 0:
        a = (a + m * int(abs(a) / m) + m) % m

    # no mod inverse if a & m aren't
    # relatively prime
    if gcd(a, m) != 1:
        return None

    # Calculate using the Extended
    # Euclidean Algorithm:
    u1 = 1
    u2 = 0
    u3 = a
    v1 = 0
    v2 = 1
    v3 = m
    while v3 != 0:
        # // is the integer division operator
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m
# ----------------------------------------------------------------
def applyDoubleAndAddMethod(P, k, a, d, mod):
    additionPoint = (P[0], P[1])
    kAsBinary = bin(k)
    Bin_k_Len = len(kAsBinary)
    kAsBinary = kAsBinary[2:Bin_k_Len]

    for i in range(1, len(kAsBinary)):
        currentBit = kAsBinary[i: i + 1]

        # always apply doubling
        additionPoint = pointAddition(additionPoint, additionPoint, a, d, mod)

        if currentBit == '1':
            # add base point
            additionPoint = pointAddition(additionPoint, P, a, d, mod)

    return additionPoint
# ----------------------------------------------------------------
# Point Addition - Function - 3d point
def pointAddition(P, Q, a, d, mod):
    x1, y1 = P[0], P[1]
    x2, y2 = Q[0], Q[1]
    # -----------
    y3_part1 = ((y1 * y2 - a * x1 * x2) % mod)
    y3_part2 = findModInverse(1 - d * x1 * x2 * y1 * y2, mod)
    # -----------
    x3_part1 = ((x1 * y2 + y1 * x2) % mod)
    x3_part2 = findModInverse(1 + d * x1 * x2 * y1 * y2, mod)
    return (x3_part1 * x3_part2) % mod, (y3_part1 * y3_part2) % mod
# ----------------------------------------------------------------
# ax^2 + y^2 = 1 + dx^2y^2
# ed25519
a = -1;
d = findPositiveModulus(-121665 * findModInverse(121666, p), p)
# print("curve: ",a,"x^2 + y^2 = 1 + ",d,"x^2 y^2")
x0, y0 = base[0], base[1]
# ----------------------------------------------------------------
# Appropriate format for XRPL addresses
value = 256
privateKey = random.getrandbits(value)
publicKey = applyDoubleAndAddMethod(base, privateKey, a, d, p)
print("Public Key:")
print(publicKey)
print("Private Key:")
print(privateKey)
# ----------------------------------------------------------------
with open('transaction.json', 'r') as f:
    XRPL_transaction = json.load(f)
# https://www.w3schools.com/python/ref_string_join.asp
concatenated_string = ''.join([str(value) for value in XRPL_transaction.values()])
message = textToInt(concatenated_string)
# ----------------------------------------------------------------
# Hashing the message/ transaction with sha512-half
# source: https://stackoverflow.com/questions/49707152/understand-what-hexdigest-do
def hashing(message):
    message_To_Str = str(message)
    message_To_Bytes = message_To_Str.encode()
    sha512 = hashlib.sha512(message_To_Bytes).digest()
    sha512half_1 = sha512[:32]
    sha512half = int(sha512half_1.hex(), 16)
    return sha512half
# ----------------------------------------------------------------
# EDDSA Sign - formulas:
# https://cryptobook.nakov.com/digital-signatures/eddsa-and-ed25519
r = hashing(hashing(privateKey) + message) % p
R = applyDoubleAndAddMethod(base, r, a, d, p)
h = hashing(R[0] + publicKey[0] + message) % p
s = r + h * privateKey
# ----------------------------------------------------------------
print("----------------------")
print("EDDSA SIGN:")
print("msg:", message)
print("Parts of the signature:")
print("R:", R)
print("s:", s)
# ----------------------------------------------------------------
# EDDSA Verify - formulas:
# https://cryptobook.nakov.com/digital-signatures/eddsa-and-ed25519
h = hashing(R[0] + publicKey[0] + message) % p
P1 = applyDoubleAndAddMethod(base, s, a, d, p)
p2_value = applyDoubleAndAddMethod(publicKey, h, a, d, p)
P2 = pointAddition(R, p2_value, a, d, p)
# ----------------------------------------------------------------
print("----------------------")
print("Verification:")
print("P1: ", P1)
print("P2: ", P2)
print("----------------------")
print("result")
if P1[0] == P2[0] and P1[1] == P2[1]:
    print("The Signature is valid")
else:
    print("Signature violation detected!")
# ----------------------------------------------------------------
EDDSA_Points = {
    'p1_0': P1[0],
    'p1_1': P1[1],
    'p2_0': P2[0],
    'p2_1': P2[1]
}
with open('/Users/sotirispittokopitis/PycharmProjects/SpartanTest_151/Task__3/circuits/points.json', 'w') as f:
    json.dump(EDDSA_Points, f)
# ----------------------------------------------------------------

