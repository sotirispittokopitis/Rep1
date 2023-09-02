# Rep1
# ZKP on XRPL

# Table of Contents
1. [Overview of the Project](#Overview-of-the-Project)
2. [Required Installations](#required-installations)


# Overview of the Project:

- Use existing crypto libraries to implement ZKP for direct XRP payment transactions. 
- For each transaction, XPRL needs to verify that the transaction is valid. In this project, you need to implement ZKP to verify the transaction on XRPL without leaking any useful information. 
	- In particular, you are required to implement the following three computations. 
		-      a. Confirm that the sender has a high enough XRP balance to send the payment.
		-      b. Confirm that the destination address is different than the sender address.
		-      c. Confirm that the signature is valid

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

















