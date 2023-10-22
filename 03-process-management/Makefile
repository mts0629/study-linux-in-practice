CC := gcc

BIN_DIR := bin
SRC_DIR := src

TARGETS := $(BIN_DIR)/fork \
	$(BIN_DIR)/fork_and_exec

RM := rm -rf

.PHONY: all mkbin clean

all: mkbin $(TARGETS)

mkbin:
	@mkdir -p $(BIN_DIR)

$(BIN_DIR)/%: $(SRC_DIR)/%.c
	$(CC) $< -o $@

clean:
	$(RM) $(BIN_DIR)
