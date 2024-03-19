
#Makefile
#Peter Grossmann
#13 September 2022
#$Id$
#$Log$

OBJECT_DIR = obj_dir
TEST_DATA_WIDTH ?= 16
TEST_NUM_COEFFS ?= 8
NUM_TEST_VECTORS ?= 100

VERILATOR_OPTIONS = 	-Wall \
			-Wno-PINCONNECTEMPTY \
			-cc \
			--exe \
			--trace \
			--top-module umi_fir_filter_test \
			-I../rtl \
			-I../include/umi/umi/umi/rtl/ \
			-CFLAGS "-Wno-unknown-warning-option -I../../include/switchboard/switchboard/cpp" \
			-LDFLAGS -pthread \
			-DFIR_FILTER_CONSTANT_COEFFS \
			-DVECTOR_COUNT_MAX=$(NUM_TEST_VECTORS) \

HDL_TOP_SOURCE = ./umi_fir_filter_test.v

HDL_SOURCE = 	../rtl/umi_fir_filter.v \
		../rtl/umi_fir_filter_regs.v \
		../rtl/fir_filter.v \
		../rtl/tree_adder.v \
		./umi_device_interface.v \
		../include/umi/umi/umi/rtl/umi_endpoint.v \
		../include/umi/umi/umi/rtl/umi_pack.v \
		../include/umi/umi/umi/rtl/umi_unpack.v \
		../include/umi/umi/umi/rtl/umi_decode.v \
		../include/lambdalib/lambdalib/stdlib/rtl/la_rsync.v \
		../include/switchboard/switchboard/verilog/sim/umi_rx_sim.sv \
		../include/switchboard/switchboard/verilog/sim/umi_tx_sim.sv \
		../include/switchboard/switchboard/verilog/sim/sb_rx_sim.sv \
		../include/switchboard/switchboard/verilog/sim/sb_tx_sim.sv \
		../include/switchboard/switchboard/verilog/sim/queue_to_sb_sim.sv \
		../include/switchboard/switchboard/verilog/sim/sb_to_queue_sim.sv \
		../include/switchboard/switchboard/verilog/sim/queue_to_umi_sim.sv \
		../include/switchboard/switchboard/verilog/sim/umi_to_queue_sim.sv \

$(OBJECT_DIR)/Vumi_fir_filter_test: $(HDL_TOP_SOURCE) $(HDL_SOURCE) config.vlt ../include/switchboard/switchboard/dpi/switchboard_dpi.cc umi_fir_filter_test.cc
	python3 generate_vectors.py $(TEST_DATA_WIDTH) $(NUM_TEST_VECTORS)
	verilator $(VERILATOR_OPTIONS) --trace config.vlt $(HDL_TOP_SOURCE) $(HDL_SOURCE) ../include/switchboard/switchboard/dpi/switchboard_dpi.cc umi_fir_filter_test.cc
	make -C $(OBJECT_DIR) -j -f Vumi_fir_filter_test.mk

clean:
	rm -rf logs obj_dir a.out *.dat *.q *.vcd *~
