// ******************************************************
// ************* Get the Preferred Network **************
// ******************************************************   
// The code for "ripplex1-send-xrp.js" and "1.get-accounts-send-xrp.html"
// ...are taken from the git repository and modified:
// https://github.com/XRPLF/xrpl-dev-portal
// (further referencing required)

function getNet() {
  let net
  if (document.getElementById("tn").checked) net = "wss://s.altnet.rippletest.net:51233"
  if (document.getElementById("dn").checked) net = "wss://s.devnet.rippletest.net:51233"
  return net
} // End of getNet()
              
// *******************************************************
// ************* Get Account *****************************
// *******************************************************

async function getAccount(type) {
  let net = getNet()
      
  const client = new xrpl.Client(net)
  results = 'Connecting to ' + net + '....'
        
// This uses the default faucet for Testnet/Devnet
  let faucetHost = null

  if (type == 'standby') {
    standbyResultField.value = results
  } else {
    operationalResultField.value = results
  }
  await client.connect()
        
  results += '\nConnected, funding wallet.'
  if (type == 'standby') {
    standbyResultField.value = results
  } else {
    operationalResultField.value = results
  }

// -----------------------------------Create and fund a test account wallet
  const my_wallet = (await client.fundWallet(null, { faucetHost })).wallet
        
  results += '\nGot a wallet.'
  if (type == 'standby') {
    standbyResultField.value = results
  } else {
    operationalResultField.value = results
  }       
      
// ------------------------------------------------------Get the current balance.
  const my_balance = (await client.getXrpBalance(my_wallet.address))  
        
  if (type == 'standby') {
    standbyAccountField.value = my_wallet.address
    standbyPubKeyField.value = my_wallet.publicKey
    standbyPrivKeyField.value = my_wallet.privateKey
    standbyBalanceField.value = (await client.getXrpBalance(my_wallet.address))
    standbySeedField.value = my_wallet.seed
    results += '\nStandby account created.'
    standbyResultField.value = results
  } else {
    operationalAccountField.value = my_wallet.address
    operationalPubKeyField.value = my_wallet.publicKey
    operationalPrivKeyField.value = my_wallet.privateKey
    operationalSeedField.value = my_wallet.seed
    operationalBalanceField.value = (await client.getXrpBalance(my_wallet.address))
    results += '\nOperational account created.'
    operationalResultField.value = results
  }
// --------------- Capture the seeds for both accounts for ease of reload.
  seeds.value = standbySeedField.value + '\n' + operationalSeedField.value
  client.disconnect()
} // End of getAccount()
      
// *******************************************************
// ********** Get Accounts from Seeds ******************** 
// *******************************************************

async function getAccountsFromSeeds() {
  let net = getNet()
  const client = new xrpl.Client(net)
  results = 'Connecting to ' + getNet() + '....'
  standbyResultField.value = results
  await client.connect()
  results += '\nConnected, finding wallets.\n'
  standbyResultField.value = results
      
// -------------------------------------------------Find the test account wallets.    
  var lines = seeds.value.split('\n')
  const standby_wallet = xrpl.Wallet.fromSeed(lines[0])
  const operational_wallet = xrpl.Wallet.fromSeed(lines[1])
      
// -------------------------------------------------------Get the current balance.
  const standby_balance = (await client.getXrpBalance(standby_wallet.address))  
  const operational_balance = (await client.getXrpBalance(operational_wallet.address))  
        
// ----------------------Populate the fields for Standby and Operational accounts.
  standbyAccountField.value = standby_wallet.address
  standbyPubKeyField.value = standby_wallet.publicKey
  standbyPrivKeyField.value = standby_wallet.privateKey
  standbySeedField.value = standby_wallet.seed
  standbyBalanceField.value = (await client.getXrpBalance(standby_wallet.address))
      
  operationalAccountField.value = operational_wallet.address
  operationalPubKeyField.value = operational_wallet.publicKey
  operationalPrivKeyField.value = operational_wallet.privateKey
  operationalSeedField.value = operational_wallet.seed
  operationalBalanceField.value = (await client.getXrpBalance(operational_wallet.address))
      
  client.disconnect()
            
} // End of getAccountsFromSeeds()

// *******************************************************
// ******************** Send XRP *************************
// *******************************************************

async function sendXRP() {    
  results  = "Connecting to the selected ledger.\n"
  standbyResultField.value = results
  let net = getNet()
  results = 'Connecting to ' + getNet() + '....'
  const client = new xrpl.Client(net)
  await client.connect()
      
  results  += "\nConnected. Sending XRP.\n"
  standbyResultField.value = results
      
  const standby_wallet = xrpl.Wallet.fromSeed(standbySeedField.value)
  const operational_wallet = xrpl.Wallet.fromSeed(operationalSeedField.value)
  const sendAmount = standbyAmountField.value
        
  results += "\nstandby_wallet.address: = " + standby_wallet.address
  standbyResultField.value = results
      
// -------------------------------------------------------- Prepare transaction
  const prepared = await client.autofill({
    "TransactionType": "Payment",
    "Account": standby_wallet.address,
    "Amount": xrpl.xrpToDrops(sendAmount),
    "Destination": standbyDestinationField.value
  })
      
// ------------------------------------------------- Sign prepared instructions
  const signed = standby_wallet.sign(prepared)
  
// -------------------------------------------------------- Submit signed blob
  const tx = await client.submitAndWait(signed.tx_blob)
      
  results  += "\nBalance changes: " + 
    JSON.stringify(xrpl.getBalanceChanges(tx.result.meta), null, 2)
        // ------------------------------------------------------------ TEST
  const standby_balance = await client.getXrpBalance(standby_wallet.address);
  results += "\nStandby_Balance: " + standby_balance;
    // ---------------------------
  const sendAmount1 = standbyAmountField.value;
  results += "\nstandby_wallet.address: = " + standby_wallet.address;
  results += "\nSending amount: " + sendAmount1 + " XRP";
  // ------------------------------------------------------------
  const jsonData = {
    sender_balance: parseInt(standby_balance, 10) * 1000000,
    transaction_amount: parseInt(sendAmount1, 10) * 1000000,
  };
  //https://stackoverflow.com/questions/26158468/create-json-file-using-blob
  const blob = new Blob([JSON.stringify(jsonData, null, 2)], { type: 'application/json' });
  const fileA = document.createElement('fileA');
  fileA.href = URL.createObjectURL(blob);
  fileA.download = 'input.json';
  document.body.appendChild(fileA);
  fileA.click();
  document.body.removeChild(fileA);
  // ------------------------------------------------------------
  standbyResultField.value = results
  standbyBalanceField.value =  (await client.getXrpBalance(standby_wallet.address))
  operationalBalanceField.value = (await client.getXrpBalance(operational_wallet.address))                 
  client.disconnect()    
} // End of sendXRP()
   
// **********************************************************************
// ****** Reciprocal Transactions ***************************************
// **********************************************************************
      
// *******************************************************
// ********* Send XRP from Operational account ***********
// *******************************************************
      
async function oPsendXRP() {

  results  = "Connecting to the selected ledger.\n"
  operationalResultField.value = results
  let net = getNet()
  results = 'Connecting to ' + getNet() + '....'
  const client = new xrpl.Client(net)
  await client.connect()
      
  results  += "\nConnected. Sending XRP.\n"
  operationalResultField.value = results
      
  const operational_wallet = xrpl.Wallet.fromSeed(operationalSeedField.value)
  const standby_wallet = xrpl.Wallet.fromSeed(standbySeedField.value)
  const sendAmount = operationalAmountField.value
        
  results += "\noperational_wallet.address: = " + operational_wallet.address
  operationalResultField.value = results
      
// ---------------------------------------------------------- Prepare transaction
  const prepared = await client.autofill({
    "TransactionType": "Payment",
    "Account": operational_wallet.address,
    "Amount": xrpl.xrpToDrops(operationalAmountField.value),
    "Destination": operationalDestinationField.value
  })

// ---------------------------------------------------- Sign prepared instructions
  const signed = operational_wallet.sign(prepared)

// ------------------------------------------------------------ Submit signed blob
  const tx = await client.submitAndWait(signed.tx_blob)
      
  results  += "\nBalance changes: " +
    JSON.stringify(xrpl.getBalanceChanges(tx.result.meta), null, 2)
  // ------------------------------------------------------------------------------------------------
  // ------------------------------------------------------------------------------------------------
  // ------------------------------------------------------------------------------------------------
  // ------------------------------------------------------------------------------------------------ TEST
  //Balance:
  const operational_balance = await client.getXrpBalance(operational_wallet.address);
  results += "\nStandby_Balance: " + operational_balance;
    // ---------------------------
    //Amount + Address:
  const sendAmount2 = operationalAmountField.value;
  results += "\noperational_wallet.address: = " + operational_wallet.address;
  results += "\nSending amount: " + sendAmount2 + " XRP";
  // results += "\nXRPL sign: " + operational_wallet.sign(prepared)

  // ------------------------------------------------------------
  const jsonData = {
    sender_balance: parseInt(operational_balance, 10) * 1000000,
    transaction_amount: parseInt(sendAmount2, 10) * 1000000,
  };
  // ------------------------------------------------------------
  //https://stackoverflow.com/questions/26158468/create-json-file-using-blob
    const blob = new Blob([JSON.stringify(tx, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'transaction.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);


  // ------------------------------------------------------------------------------------------------
  // ------------------------------------------------------------------------------------------------
  // ------------------------------------------------------------------------------------------------




  // ------------------------------------------------------------------------------------------------
  // ------------------------------------------------------------------------------------------------
  // ------------------------------------------------------------------------------------------------
  operationalResultField.value = results
  standbyBalanceField.value = (await client.getXrpBalance(standby_wallet.address))
  operationalBalanceField.value = (await client.getXrpBalance(operational_wallet.address))                 
      
  client.disconnect()
      
} // End of oPsendXRP()