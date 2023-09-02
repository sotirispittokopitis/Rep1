from xrpl.core.addresscodec import decode_classic_address
import json
# links:
# https://xrpl-py.readthedocs.io/en/stable/source/xrpl.core.addresscodec.html
#

address1 = 'rEhVrA7fNgfsFB9R9ZoWJA22HaYuUX2hdt'
address2 = 'r3J5WiRzJW3PvnsagpXVM8x7MVNucC7Dqm'
# ---------------------------- Bit Format
decoded1 = decode_classic_address(address1)
decoded2 = decode_classic_address(address2)
print('Decoded in Bit-format:')
print(decoded1)
print(decoded2)
# ---------------------------- Hex Format
print('Decoded in Hex-format:')
decoded_hex1 = decoded1.hex()
decoded_hex2 = decoded2.hex()
print(decoded_hex1)
print(decoded_hex2)
# ---------------------------- BigInt Format
add_bigInt1 = int(decoded_hex1, 16)
add_bigInt2 = int(decoded_hex2, 16)
print('Decoded in bigInt-format:')
print(add_bigInt1)
print(add_bigInt2)
# ---------------------------- Make json file
Address_Data = {
    'sender_Address_1': add_bigInt1,
    'destination_Address_2': add_bigInt2
}
with open('/Users/sotirispittokopitis/PycharmProjects/SpartanTest_151/test2/input_task2.json', 'w') as f:
    json.dump(Address_Data, f)










