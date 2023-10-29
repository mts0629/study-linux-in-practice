CC := gcc

BIN_DIR := bin
SRC_DIR := src

TARGETS := $(BIN_DIR)/cache

RM := rm -rf

.PHONY: all mkbin clean

all: mkbin $(TARGETS)

mkbin:
	@mkdir -p $(BIN_DIR)

$(BIN_DIR)/cache: $(SRC_DIR)/cache.c
	$(CC) -O3 $< -o $@

$(BIN_DIR)/%: $(SRC_DIR)/%.c
	$(CC) $< -o $@

clean:
	$(RM) $(BIN_DIR)
