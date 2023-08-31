include "/Users/sotirispittokopitis/PycharmProjects/SpartanTest_151/node_modules/circomlib/circuits/comparators.circom";

template circuitTask3() {
    signal input p1_0;
    signal input p1_1;
    signal input p2_0;
    signal input p2_1;

    signal output validation;

    component isEqual_px = IsEqual();
    component isEqual_py = IsEqual();

    isEqual_px.in[0] <== p1_0;
    isEqual_px.in[1] <== p2_0;

    isEqual_py.in[0] <== p1_1;
    isEqual_py.in[1] <== p2_1;

    validation <== isEqual_px.out * isEqual_py.out;
}

component main = circuitTask3();

