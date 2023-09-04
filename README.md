# ZKP on XRPL
- Use existing libraries to implement ZKP for XRP payment transactions. 

# Table of Contents
1. [Overview of the Project](#Overview-of-the-Project)
2. [Required Installations](#required-installations)
3. [Running the Code](#running-the-code)
4. [Time Benchmarks](#time-Benchmarks)


# Overview of the Project:

For this project, we introduce a strategy to integrate Zero-Knowledge Proofs (ZKPs) within the XRP Ledger (XRPL) with the goal of verifying the transactions on XRP Ledger without leaking any useful information. Since the XRP Ledger currently does not offer support for Zero-Knowledge Proofs (ZKPs) we provide further details on the structure we use to emulate the EdDSA operations that the XRP Ledger currently uses, specifically on the ed255519 elliptic curve. Furthermore, we implement the following three computations:

- Confirm that the sender has a high enough XRP balance to send the payment.
- Confirm that the destination address is different than the sender address.
- Confirm that the signature is valid.

Disclaimer: The following implementations are for demonstration purposes only. Furthermore, the circuits are not audited, and should not be used for production-grade applications at their current state.

# Required Installations:

Instructions can be found at:
- [Circom Documentation](https://docs.circom.io/getting-started/installation/)
- [CircomLib GitHub Repository](https://github.com/iden3/circomlib/tree/master)

## Installing Circom
**Step 1:**  
Clone the “Circom” repository:
```bash
git clone --recurse-submodules https://github.com/iden3/circom.git
```

**Step 2:**  
Change to the `circom` directory and build the release:
```bash
cd circom
cargo build --release
```

**Step 3:**  
Install the circom binary:
```bash
cargo install --path circom
```
## Installing snarkjs
**Step 1:**  
```bash
npm install -g snarkjs
```
## Installing Circom-Lib
**Step 1:**  
Clone the “Circom” repository:
```bash
git clone --recurse-submodules https://github.com/iden3/circomlib/tree/master
```

# Running the Code:
- task_1 & task_2: They each have a `build.py` file. When running the Python file, it will generate and verify a ZKP
- task_3: There are two python files that can be run. The first one is `build.py` and the second one is `build_python.py`, where the former will generate and verify the ZKP, while the latter will run a server-clent environment, run EDDSA operations, as well as generate and verify the ZKP 


# Time Benchmarks:

|                                | Time Taken (s) - Circuit 1 | Time Taken (s) - Circuit 2 | Time Taken (s) - Circuit 3 |
|--------------------------------|----------------------------|----------------------------|----------------------------|
| Compiling Circuit              | 0                          | 0                          | 1                          |
| Exporting R1CS to JSON         | 1                          | 1                          | 0                          |
| Generating Witness             | 0                          | 0                          | 0                          |
| Exporting Witness to JSON      | 0                          | 0                          | 1                          |
| Generating New Powers of Tau   | 1                          | 1                          | 0                          |
| Contributing To Powers of Tau  | 3                          | 3                          | 5                          |
| Preparing Phase 2              | 27                         | 28                         | 31                         |
| Generating ZKey 0              | 2                          | 1                          | 1                          |
| Generating ZKey 1              | 1                          | 1                          | 2                          |
| Exporting Verification Key     | 1                          | 1                          | 1                          |
| Generating Proof               | 0                          | 0                          | 0                          |
| Verifying ZKey                 | 2                          | 2                          | 2                          |
| Total Time                     | ~39s                       | ~38s                       | ~45s                       |

















