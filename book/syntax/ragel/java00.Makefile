SRC = app/src/main/java/
PKG = $(SRC)/io/github/ponyatov/metal
$(PKG)/FORTH.java: FORTH.ragel Makefile
	ragel -J -o $@ $<
