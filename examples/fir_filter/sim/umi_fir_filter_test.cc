//umi_fir_filter_test.cc
//Peter Grossmann
//6 October 2023
//$Id$
//$Log$

//Adapted from:
//https://github.com/tommythorn/verilator-demo/blob/master/sim_main.cpp

#include <iostream>
#include <string>

#include "Vumi_fir_filter_test.h"
#include "verilated.h"

//Adapted from /usr/share/doc/verilator/examples/make_tracing_c/sim_main.cpp
//distributed with Verilator 4.028 2020-02-06 rev v4.026-92-g890cecc1
//Other #if VM_TRACE blocks adapted from this source as well
// If "verilator --trace" is used, include the tracing class
#if VM_TRACE
# include <verilated_vcd_c.h>
#endif

int main(int argc, char **argv, char **env) {
  
  Verilated::commandArgs(argc, argv);
  Verilated::traceEverOn(true);
    
  Vumi_fir_filter_test *dut = new Vumi_fir_filter_test;

#if VM_TRACE
  // If verilator was invoked with --trace argument,
  // and if at run time passed the +trace argument, turn on tracing
  VerilatedVcdC* tfp = NULL;
  const char* flag = Verilated::commandArgsPlusMatch("trace");
  if (flag && 0==strcmp(flag, "+trace")) {
    Verilated::traceEverOn(true);  // Verilator must compute traced signals
    VL_PRINTF("Enabling waves into logs/umi_fir_filter_test.vcd...\n");
    tfp = new VerilatedVcdC;
    dut->trace(tfp, 99);  // Trace 99 levels of hierarchy
    Verilated::mkdir("logs");
    tfp->open("logs/umi_fir_filter_test.vcd");  // Open the dump file
  }
#endif
  
  int sim_time = 0;
  dut->clk = 0;
  dut->resetn = 1;
  dut->eval();
  while(!Verilated::gotFinish()) {
    if ((sim_time >= 1) && (sim_time <= 10)) {
      dut->resetn = 0;
    }
    else {
      if (sim_time > 10) {
	dut->resetn = 1;
      }
    }

    if (sim_time % 5 == 0) {
      dut->clk ^= 1;
    }
    dut->eval();
    
#if VM_TRACE
    // Dump trace data for this cycle
    if (tfp) tfp->dump(sim_time);
#endif
    
    sim_time ++;
  }
  dut->final();

  // Close trace if opened
#if VM_TRACE
    if (tfp) { tfp->close(); tfp = NULL; }
#endif

  delete dut;
  exit(0);

}
