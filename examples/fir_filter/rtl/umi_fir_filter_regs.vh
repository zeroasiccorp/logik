
//The UMI FIR filter design makes use of
//three configuration registers, each of which
//is accessed with a 2-bit address.

//Control register
parameter CTRL_REG_ADDR = 2'b00;
//Coefficient register
parameter COEFF_REG_ADDR = 2'b01;
//Sample register
parameter SAMPLE_REG_ADDR = 2'b10;
