#---------------------------------------------------------------------------
# SETUP
#---------------------------------------------------------------------------
PYTHON3           := /usr/bin/env python3
REPO_LIB          := $(PWD)/../lib
TMPDIR_BASENAME   := TMP
ENV_RUNNER        := /usr/bin/env PYTHONPATH=$(REPO_LIB):$(PWD)/lib PYTHONDONTWRITEBYTECODE=1 TMPDIR_BASENAME=$(TMPDIR_BASENAME)
PYTHON_RUNNER     := $(ENV_RUNNER) $(PYTHON3)
UNIT_TESTS        := $(foreach file, $(shell find unit_tests -name '*.py'), $(file)-py)

#---------------------------------------------------------------------------
# FUNCTIONS
#---------------------------------------------------------------------------
define run_with_python
	$(PYTHON_RUNNER) $(1)
endef

#---------------------------------------------------------------------------
# TARGETS
#---------------------------------------------------------------------------
%-py:
	$(call run_with_python, $*)

sanity: $(UNIT_TESTS)

clean:
	rm -rf $(PWD)/$(TMPDIR_BASENAME)
