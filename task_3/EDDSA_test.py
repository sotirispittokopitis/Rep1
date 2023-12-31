import hashlib
import json
import random
# The following code is taken from:
# https://www.geeksforgeeks.org/blockchain-elliptic-curve-digital-signature-algorithm-ecdsa/
# Although some formulas/parts remain the same, some alterations are added to simulate the XRPL
# (further referencing required)

# ----------------------------------------------------------------
part_pow = pow(2, 255)
p = part_pow - 19

partA = 15112221349535400772501151409588531511454012693041857206046113283949847762202
partB = 46316835694926478169428394003475163141307993866256225615783033603165251855960
G = partA,partB
# ----------------------------------------------------------------
def mod_Possitive(a, p):
    if a < 0:
        part1 = p * int(abs(a) * 1/p)
    return (a + part1 + p) % p
# ----------------------------------------------------------------
def from_Txt_to_Int(txt):
    encode1 = txt.encode()
    hex1 = encode1.hex()
    return int(hex1, 16)
# ----------------------------------------------------------------

def Greatest_Common_Divisor(a, b):
    while a != 0:
        value1 = a
        value2 = b
        theRemainder = value2 % value1
        a = theRemainder
        b = value1
    return b
# ----------------------------------------------------------------
def inverse_Modulo(a, m):
    if a < 0:
        part1 = int(abs(a) * 1/m)
        part2 = m * part1
        a = (a + part2 + m) % m

    if Greatest_Common_Divisor(a, m) != 1:
        return None

    u1 = 1
    u2 = 0
    u3 = a
    v1 = 0
    v2 = 1
    v3 = m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
        answ = u1 % m
    return answ
# ----------------------------------------------------------------
def double_And_Add(P, k, a, d, mod):
    additionPoint = (P[0], P[1])
    k_toBin = bin(k)
    Bin_k_Len = len(k_toBin)
    k_toBin = k_toBin[2:Bin_k_Len]
    len2 = len(k_toBin)
    for i in range(1, len2 ):
        currentBit = k_toBin[i: i + 1]

        additionPoint = apply_Point_add(additionPoint, additionPoint, a, d, mod)

        if currentBit == '1':
            additionPoint = apply_Point_add(additionPoint, P, a, d, mod)

    return additionPoint
# ----------------------------------------------------------------
# Point Addition - Function - 3d point
def apply_Point_add(P, Q, a, d, mod):
    x1, y1 = P[0], P[1]
    x2, y2 = Q[0], Q[1]
    # -----------
    y3_part1 = ((y1 * y2 - a * x1 * x2) % mod)
    y3_part2 = inverse_Modulo(1 - d * x1 * x2 * y1 * y2, mod)
    # -----------
    x3_part1 = ((x1 * y2 + y1 * x2) % mod)
    x3_part2 = inverse_Modulo(1 + d * x1 * x2 * y1 * y2, mod)
    return (x3_part1 * x3_part2) % mod, (y3_part1 * y3_part2) % mod
# ----------------------------------------------------------------
a = -1;

kk = -121665
d = mod_Possitive(kk * inverse_Modulo(121666, p), p)
x0, y0 = G[0], G[1]
# ----------------------------------------------------------------
# Appropriate format for XRPL addresses
value = 256
privateKey = random.getrandbits(value)
publicKey = double_And_Add(G, privateKey, a, d, p)
print("Public Key:")
print(publicKey)
print("Private Key:")
print(privateKey)
# ----------------------------------------------------------------
with open('transaction.json', 'r') as f:
    XRPL_transaction = json.load(f)
# https://www.w3schools.com/python/ref_string_join.asp
v_toStr = [str(value) for value in XRPL_transaction.values()]
conc_str = ''.join(v_toStr)
message = from_Txt_to_Int(conc_str)
# ----------------------------------------------------------------
# Hashing the message/ transaction with sha512-half
# source: https://stackoverflow.com/questions/49707152/understand-what-hexdigest-do
def apply_Hash(message):
    message_To_Str = str(message)
    message_To_Bytes = message_To_Str.encode()
    sha512 = hashlib.sha512(message_To_Bytes).digest()
    sha512half_1 = sha512[:32]
    sha512half = int(sha512half_1.hex(), 16)
    return sha512half
# ----------------------------------------------------------------
# EDDSA Sign - formulas:

# https://cryptobook.nakov.com/digital-signatures/eddsa-and-ed25519
r = apply_Hash(apply_Hash(privateKey) + message) % p
R = double_And_Add(G, r, a, d, p)
h = apply_Hash(R[0] + publicKey[0] + message) % p
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
h = apply_Hash(R[0] + publicKey[0] + message) % p
the_Point1 = double_And_Add(G, s, a, d, p)
p2_value = double_And_Add(publicKey, h, a, d, p)
the_Point2 = apply_Point_add(R, p2_value, a, d, p)
# ----------------------------------------------------------------
print("----------------------")
print("Values of P_1 + P_2:")
print(the_Point1)
print(the_Point2)
print("----------------------")
if the_Point1[0] == the_Point2[0] and the_Point1[1] == the_Point2[1]:
    print("The Signature is valid")
else:
    print("Signature violation detected!")
# ----------------------------------------------------------------
EDDSA_Points = {
    'p1_0': the_Point1[0],
    'p1_1': the_Point1[1],
    'p2_0': the_Point2[0],
    'p2_1': the_Point2[1]
}
with open('../task_3/circuit/input.json', 'w') as f:
    json.dump(EDDSA_Points, f)
# ----------------------------------------------------------------

