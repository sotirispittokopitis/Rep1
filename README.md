# ZKP on XRPL
- Use existing crypto libraries to implement ZKP for XRP payment transactions. 

# Table of Contents
1. [Overview of the Project](#Overview-of-the-Project)
2. [Required Installations](#required-installations)


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

















