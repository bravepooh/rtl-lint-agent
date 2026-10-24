# Behavioral tests for the agent's demo targets. The gate runs:  make TOP=<module> SRC=<candidate.sv>
SIM ?= icarus
TOP ?= sat_add
SRC ?= $(abspath ../$(TOP).sv)

TOPLEVEL_LANG       = verilog
VERILOG_SOURCES     = $(SRC)
COCOTB_TOPLEVEL     = $(TOP)
COCOTB_TEST_MODULES = test_$(TOP)
SIM_BUILD           ?= sim_build/$(TOP)
COCOTB_RESULTS_FILE ?= results_$(TOP).xml
COMPILE_ARGS        += -g2012

include $(shell cocotb-config --makefiles)/Makefile.sim
