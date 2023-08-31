#!/bin/bash

# https://github.com/0xPARC/circom-ecdsa

CIRCUIT_NAME=mult
INPUT_JSON=input.json
PTAU_NAME=pot12

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
TARGET_DIR="$SCRIPT_DIR/circuit"
mkdir -p $TARGET_DIR

echo "****COMPILING CIRCUIT****"
circom $SCRIPT_DIR/$CIRCUIT_NAME.circom --r1cs --wasm --sym --c --wat --output "$TARGET_DIR"

echo "****MOVING FILES****"
mv $TARGET_DIR/mult_js/* $TARGET_DIR

echo "****EXPORTING R1CS TO JSON****"
snarkjs r1cs export json $TARGET_DIR/$CIRCUIT_NAME.r1cs $TARGET_DIR/$CIRCUIT_NAME.json

echo "****GENERATING WITNESS****"
node $TARGET_DIR/generate_witness.js $TARGET_DIR/$CIRCUIT_NAME.wasm $SCRIPT_DIR/$INPUT_JSON $TARGET_DIR/witness.wtns

echo "****EXPORTING WITNESS TO JSON****"
snarkjs wtns export json $TARGET_DIR/witness.wtns $TARGET_DIR/witness.json

echo "****GENERATING NEW POWERS OF TAU****"
snarkjs powersoftau new bn128 12 $TARGET_DIR/$PTAU_NAME"_0000.ptau" -v

echo "****CONTRIBUTING TO POWERS OF TAU****"
echo "qwe" | npx snarkjs powersoftau contribute $TARGET_DIR/$PTAU_NAME"_0000.ptau" $TARGET_DIR/$PTAU_NAME"_0001.ptau" --name="My name" -v

echo "****PREPARING PHASE 2****"
snarkjs powersoftau prepare phase2 $TARGET_DIR/$PTAU_NAME"_0001.ptau" $TARGET_DIR/$PTAU_NAME"_final.ptau" -v

echo "****GENERATING ZKEY 0****"
snarkjs groth16 setup $TARGET_DIR/$CIRCUIT_NAME.r1cs $TARGET_DIR/$PTAU_NAME"_final.ptau" $TARGET_DIR/$CIRCUIT_NAME"_0000.zkey"

echo "****GENERATING ZKEY 1****"
echo "test" | npx snarkjs zkey contribute $TARGET_DIR/$CIRCUIT_NAME"_0000.zkey" $TARGET_DIR/$CIRCUIT_NAME"_0001.zkey" --name="Test Name" -v

echo "****EXPORTING VERIFICATION KEY****"
snarkjs zkey export verificationkey $TARGET_DIR/$CIRCUIT_NAME"_0001.zkey" $TARGET_DIR/verification_key.json

echo "****GENERATING PROOF****"
snarkjs groth16 prove $TARGET_DIR/$CIRCUIT_NAME"_0001.zkey" $TARGET_DIR/witness.wtns $TARGET_DIR/proof.json $TARGET_DIR/public.json

echo "****VERIFYING ZKEY****"
snarkjs zkey verify $TARGET_DIR/$CIRCUIT_NAME.r1cs $TARGET_DIR/$PTAU_NAME"_final.ptau" $TARGET_DIR/$CIRCUIT_NAME"_0000.zkey"
