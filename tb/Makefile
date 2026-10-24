# cocotb testbenches. One design per run:  make TOP=sync_fifo   |   make TOP=async_fifo
# SIM defaults to Icarus (what CI uses). Verilator also works locally: make SIM=verilator

SIM ?= icarus
TOP ?= sync_fifo
SRC ?= $(abspath ../rtl/$(TOP).sv)

TOPLEVEL_LANG       = verilog
VERILOG_SOURCES     = $(SRC)
COCOTB_TOPLEVEL     = $(TOP)
COCOTB_TEST_MODULES = test_$(TOP)
SIM_BUILD           = sim_build/$(TOP)
COCOTB_RESULTS_FILE = results_$(TOP).xml

ifeq ($(SIM),icarus)
COMPILE_ARGS += -g2012
endif
ifeq ($(SIM),verilator)
EXTRA_ARGS += -Wno-fatal
endif

include $(shell cocotb-config --makefiles)/Makefile.sim
