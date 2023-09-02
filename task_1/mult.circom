include "/Users/sotirispittokopitis/PycharmProjects/SpartanTest_151/node_modules/circomlib/circuits/comparators.circom";

template BalanceCheck() {
    signal input sender_balance;
    signal input transaction_amount;

    signal output valid;

    component comp = GreaterThan(192);
    comp.in[0] <== sender_balance;
    comp.in[1] <== transaction_amount;

    valid <== comp.out;
}
 component main = BalanceCheck();
