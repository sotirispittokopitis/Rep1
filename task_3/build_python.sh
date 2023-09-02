#!/bin/bash
# The idea is taken from the following links:
# https://github.com/0xPARC/circom-ecdsa
# https://www.guru99.com/introduction-to-shell-scripting.html
echo "-------------------------------------------------------"
CIRCUIT_NAME=mult
INPUT_JSON=input.json
PTAU_NAME=pot12
echo "-------------------------------------------------------"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
TARGET_DIR="$SCRIPT_DIR/server_client"
mkdir -p $TARGET_DIR
echo "-------------------------------------------------------"
echo ">>Step_1:"
echo ">>Start Server..."
python server.py &
sleep 4
echo "-------------------------------------------------------"
echo ">>Step_2:"
echo ">>Client connects..."
sleep 1
#python client.py
echo ">>Client would make a transaction..."
sleep 2
echo ">>EDDSA opperations take place....."
python EDDSA_test.py
sleep 3
echo ">>Finished ....."
echo "-------------------------------------------------------"
echo ">>Step_3:"
echo ">>Generating proof..."
echo ">>Start:"
sleep 2
./build.sh
echo ">>Finish generating the proof:"
sleep 2
echo "-------------------------------------------------------"
echo ">>Step_4:"
echo ">>The Prover sends the neccesary files to the veriefier to validate the proof!"
sleep 2
python client.py
echo ">>The veriefier receives the files"
echo ">>The veriefier detremines if the Proof is valid!"
sleep 4
echo "-------------------------------------------------------"






