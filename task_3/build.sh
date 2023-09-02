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
TARGET_DIR="$SCRIPT_DIR/circuit"
mkdir -p $TARGET_DIR
time_sum=0
echo "-------------------------------------------------------"
echo ">>Compiling Circuit"
start=`date +%s`
circom $SCRIPT_DIR/$CIRCUIT_NAME.circom --r1cs --wasm --sym --c --wat --output "$TARGET_DIR"
end=`date +%s`
time_sum=$((time_sum + $((end-start))))
echo ">>Step Completed:"
echo "Time:($((end-start)) s)"
echo "-------------------------------------------------------"
echo ">>Moving Files"
start=`date +%s`
mv $TARGET_DIR/mult_js/* $TARGET_DIR
end=`date +%s`
time_sum=$((time_sum + $((end-start))))
echo ">>Step Completed:"
echo "Time:($((end-start)) s)"
echo "-------------------------------------------------------"
echo ">>Exporting R1CS To JSON"
start=`date +%s`
snarkjs r1cs export json $TARGET_DIR/$CIRCUIT_NAME.r1cs $TARGET_DIR/$CIRCUIT_NAME.json
end=`date +%s`
time_sum=$((time_sum + $((end-start))))
echo ">>Step Completed:"
echo "Time:($((end-start)) s)"
echo "-------------------------------------------------------"
echo ">>Generating Witness"
start=`date +%s`
node $TARGET_DIR/generate_witness.js $TARGET_DIR/$CIRCUIT_NAME.wasm $SCRIPT_DIR/$INPUT_JSON $TARGET_DIR/witness.wtns
end=`date +%s`
time_sum=$((time_sum + $((end-start))))
echo ">>Step Completed:"
echo "Time:($((end-start)) s)"
echo "-------------------------------------------------------"
echo ">>Exporting Witness To JSON"
start=`date +%s`
snarkjs wtns export json $TARGET_DIR/witness.wtns $TARGET_DIR/witness.json
end=`date +%s`
time_sum=$((time_sum + $((end-start))))
echo ">>Step Completed:"
echo "Time:($((end-start)) s)"
echo "-------------------------------------------------------"
echo ">>Generating New Powers Of Tau"
start=`date +%s`
snarkjs powersoftau new bn128 12 $TARGET_DIR/$PTAU_NAME"_0000.ptau" -v
end=`date +%s`
time_sum=$((time_sum + $((end-start))))
echo ">>Step Completed:"
echo "Time:($((end-start)) s)"
echo "-------------------------------------------------------"
echo ">>Contributing To Powers Of Tau"
start=`date +%s`
echo "qwe" | npx snarkjs powersoftau contribute $TARGET_DIR/$PTAU_NAME"_0000.ptau" $TARGET_DIR/$PTAU_NAME"_0001.ptau" --name="My Name" -v
end=`date +%s`
time_sum=$((time_sum + $((end-start))))
echo ">>Step Completed:"
echo "Time:($((end-start)) s)"
echo "-------------------------------------------------------"
echo ">>Preparing Phase 2"
start=`date +%s`
snarkjs powersoftau prepare phase2 $TARGET_DIR/$PTAU_NAME"_0001.ptau" $TARGET_DIR/$PTAU_NAME"_final.ptau" -v
end=`date +%s`
time_sum=$((time_sum + $((end-start))))
echo ">>Step Completed:"
echo "Time:($((end-start)) s)"
echo "-------------------------------------------------------"
echo ">>Generating ZKey 0"
start=`date +%s`
snarkjs groth16 setup $TARGET_DIR/$CIRCUIT_NAME.r1cs $TARGET_DIR/$PTAU_NAME"_final.ptau" $TARGET_DIR/$CIRCUIT_NAME"_0000.zkey"
end=`date +%s`
time_sum=$((time_sum + $((end-start))))
echo ">>Step Completed:"
echo "Time:($((end-start)) s)"
echo "-------------------------------------------------------"
echo ">>Generating ZKey 1"
start=`date +%s`
echo "qwe" | npx snarkjs zkey contribute $TARGET_DIR/$CIRCUIT_NAME"_0000.zkey" $TARGET_DIR/$CIRCUIT_NAME"_0001.zkey" --name="Test Name" -v
end=`date +%s`
time_sum=$((time_sum + $((end-start))))
echo ">>Step Completed:"
echo "Time:($((end-start)) s)"
echo "-------------------------------------------------------"
echo ">>Exporting Verification Key"
start=`date +%s`
snarkjs zkey export verificationkey $TARGET_DIR/$CIRCUIT_NAME"_0001.zkey" $TARGET_DIR/verification_key.json
end=`date +%s`
time_sum=$((time_sum + $((end-start))))
echo ">>Step Completed:"
echo "Time:($((end-start)) s)"
echo "-------------------------------------------------------"
echo ">>Generating Proof"
start=`date +%s`
snarkjs groth16 prove $TARGET_DIR/$CIRCUIT_NAME"_0001.zkey" $TARGET_DIR/witness.wtns $TARGET_DIR/proof.json $TARGET_DIR/public.json
end=`date +%s`
time_sum=$((time_sum + $((end-start))))
echo ">>Step Completed:"
echo "Time:($((end-start)) s)"
echo "-------------------------------------------------------"
echo ">>Verifying ZKey"
start=`date +%s`
snarkjs zkey verify $TARGET_DIR/$CIRCUIT_NAME.r1cs $TARGET_DIR/$PTAU_NAME"_final.ptau" $TARGET_DIR/$CIRCUIT_NAME"_0000.zkey"
end=`date +%s`
time_sum=$((time_sum + $((end-start))))
echo ">>Step Completed:"
echo "Time:($((end-start)) s)"
echo "-------------------------------------------------------"
echo ">>Total Time Taken: $time_sum s"
