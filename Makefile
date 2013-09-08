ifneq ($(shell id -u),0)
SUDO := sudo
endif

all:
	@echo "Run \`make' with the following target(s):"
	@echo "  ftd2xx    build python bindings and install it (root required)"
	@echo "  load      proper load ftdi_sio module to create one ttyUSB (root required)"

ftd2xx:
	cd $(CURDIR)/ftd2xx-git1; \
	    python setup.py build; \
	    $(SUDO) python setup.py install

load:
	@echo $(CURDIR)/load-ftdi.sh
	@$(SUDO) $(CURDIR)/load-ftdi.sh

.PHONY: ftd2xx load
