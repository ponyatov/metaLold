APP = desktop
HW  = miniG4
#qemu386

include app/$(APP).mk
include hw/$(HW).mk
include cpu/$(CPU).mk
include arch/$(ARCH).mk


CWD     = $(CURDIR)
MODULE  = $(shell echo $(notdir $(CWD)) | tr "[:upper:]" "[:lower:]" )
OS     ?= $(shell uname -s)

NOW = $(shell date +%d%m%y)
REL = $(shell git rev-parse --short=4 HEAD)

WGET = wget -c --no-check-certificate



BUILDROOT_VER = 2020.05
BUILDROOT     = buildroot-$(BUILDROOT_VER)
BUILDROOT_GZ  = $(BUILDROOT).tar.bz2



.PHONY: all
all: dirs gz fw emu

GZ  ?= $(HOME)/gz
TMP ?= $(CWD)/tmp
SRC ?= $(TMP)/src
FW  ?= $(CWD)/firmware

VENDOR = $(CWD)/vendor

.PHONY: dirs
dirs:
	mkdir -p $(GZ) $(TMP) $(SRC) $(FW)

.PHONY: gz
gz: $(GZ)/$(BUILDROOT_GZ)
$(GZ)/$(BUILDROOT_GZ):
	$(WGET) -O $@ https://buildroot.org/downloads/$(BUILDROOT_GZ)

XMAKE = $(MAKE) BR2_EXTERNAL=$(VENDOR)

CONFIG_BUILDROOT  = $(CWD)/all/all.buildroot $(CWD)/app/$(APP).buildroot
CONFIG_BUILDROOT += $(CWD)/arch/$(ARCH).buildroot $(CWD)/cpu/$(CPU).buildroot $(CWD)/hw/$(HW).buildroot
CONFIG_KERNEL     = $(CWD)/all/all.kernel $(CWD)/app/$(APP).kernel
CONFIG_KERNEL    += $(CWD)/arch/$(ARCH).kernel $(CWD)/cpu/$(CPU).kernel $(CWD)/hw/$(HW).kernel
CONFIG_ROOT       = $(CWD)/all/root $(CWD)/app/$(APP).root

.PHONY: build
build: $(BUILDROOT)/README
	cd $(BUILDROOT) ; $(XMAKE) distclean ; $(XMAKE) allnoconfig
	$(MAKE) rebuild

APPFILES = $(shell find app/$(APP).root -type f )

.PHONY: rebuild
rebuild: $(BUILDROOT)/output/images/bzImage
$(BUILDROOT)/output/images/bzImage: $(CONFIG_BUILDROOT) $(CONFIG_KERNEL) $(BUILDROOT)/.config $(APPFILES)
	cd $(BUILDROOT) ;\
	cat $(CONFIG_BUILDROOT) >> .config &&\
	echo "BR2_DL_DIR=\"$(TMP)\"" >> .config &&\
	echo "BR2_ROOTFS_OVERLAY=\"$(CONFIG_ROOT)\"" >> .config &&\
	echo "BR2_LINUX_KERNEL_CONFIG_FRAGMENT_FILES=\"$(CONFIG_KERNEL)\"" >> .config &&\
	echo "BR2_TARGET_GENERIC_HOSTNAME=\"$(APP)_$(HW)\"" >> .config &&\
	$(XMAKE) menuconfig       &&\
	$(XMAKE) linux-menuconfig &&\
	$(XMAKE)
	$(MAKE) fw

KERNEL = $(FW)/$(APP)_$(HW)_kernel

.PHONY: fw
fw: $(KERNEL)
$(KERNEL): $(BUILDROOT)/output/images/bzImage
	cp $< $@

.PHONY: kernel
kernel:
	cd $(BUILDROOT) ;\
	$(XMAKE) linux-menuconfig &&\
	$(XMAKE)
	$(MAKE) fw

.PHONY: emu
emu: $(KERNEL)
	qemu-system-$(ARCH) -kernel $< -append "console=ttyS0 $(QEMU_APPEND)" -serial stdio $(QEMU_ARGS)



%/README: $(GZ)/%.tar.bz2
	bzcat $< | tar x && touch $@



.PHONY: install update

install: $(OS)_install
update: $(OS)_update

.PHONY: Linux_install Linux_update

Linux_install Linux_update:
	sudo apt update
	sudo apt install -u `cat apt.txt`

.PHONY: master shadow release

MERGE  = Makefile README.md .gitignore .vscode apt.txt requirements.txt
# MERGE += $(MODULE).py $(MODULE).ini static templates
# MERGE += $(MODULE).nimble src tests

# master:
# 	git checkout $@
# 	git pull -v
# 	git checkout shadow -- $(MERGE)

# shadow:
# 	git checkout $@
# 	git pull -v

# release:
# 	git tag $(NOW)-$(REL)
# 	git push -v && git push -v --tags
# 	$(MAKE) shadow
