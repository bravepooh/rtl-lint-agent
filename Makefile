# One entry point for everything. Uses .venv/bin for cocotb if it exists.
#   make all      lint + tests + formal + gate self-test (what CI runs)
#   make agent    run the AI fix agent over demo/ (needs a model backend, see agent/model.py)

SHELL := /bin/bash
ifneq ($(wildcard .venv/bin),)
export PATH := $(CURDIR)/.venv/bin:$(PATH)
endif
PY   ?= python3
SIM  ?= icarus
LINT := verilator --lint-only -Wall

.PHONY: all lint gallery test test-demo formal synth selftest agent clean

all: lint test formal selftest

lint:
	@fail=0; for f in rtl/*.sv; do \
	  if $(LINT) $$f >/dev/null 2>&1; then echo "clean  $$f"; else echo "DIRTY  $$f"; $(LINT) $$f; fail=1; fi; \
	done; exit $$fail

# Every gallery file is expected to trigger its rule. Prints the codes Verilator reports.
gallery:
	@fail=0; for f in lint-gallery/*.sv; do \
	  codes=$$($(LINT) $$f 2>&1 | grep -oE '^%Warning-[A-Z_]+' | sed 's/%Warning-//' | sort -u | tr '\n' ' '); \
	  printf "%-24s %s\n" $$(basename $$f) "$${codes:-NO WARNING (gallery file is broken)}"; \
	  [ -n "$$codes" ] || fail=1; \
	done; exit $$fail

test:
	$(MAKE) -s -C tb TOP=sync_fifo SIM=$(SIM)
	$(MAKE) -s -C tb TOP=async_fifo SIM=$(SIM)

# The demo targets are lint-dirty on purpose but must still pass their behavior tests.
test-demo:
	@for t in demo/*.sv; do $(MAKE) -s -C demo/tests TOP=$$(basename $$t .sv) || exit 1; done

formal:
	cd formal && sby -f sync_fifo.sby

synth:
	@for t in sync_fifo async_fifo; do \
	  echo "== $$t"; yosys -q -p "read_verilog -sv rtl/$$t.sv; synth -top $$t; tee -o /dev/stdout stat" | grep -E 'cells|DFF|Number of'; \
	done

selftest:
	$(PY) agent/selftest.py

agent:
	$(PY) agent/fix.py demo/ $(ARGS)

clean:
	rm -rf tb/sim_build tb/results*.xml demo/tests/sim_build demo/tests/results*.xml \
	       formal/sync_fifo_prove formal/sync_fifo_cover obj_dir
	find . -name __pycache__ -prune -exec rm -rf {} +
