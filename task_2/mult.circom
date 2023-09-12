include "/Users/sotirispittokopitis/PycharmProjects/SpartanTest_151/node_modules/circomlib/circuits/comparators.circom";


template AddressCheck() {
    signal input sender_Address_1;
    signal input destination_Address_2;

    signal output validation;

    component isEqual = IsEqual();
    isEqual.in[0] <== sender_Address_1;
    isEqual.in[1] <== destination_Address_2;

    validation <== 1 - isEqual.out;
}
 component main = AddressCheck();
