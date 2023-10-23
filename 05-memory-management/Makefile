CC := gcc

BIN_DIR := bin
SRC_DIR := src

TARGETS := $(BIN_DIR)/cow \
	$(BIN_DIR)/demand-paging \
	$(BIN_DIR)/filemap \
	$(BIN_DIR)/mmap \
	$(BIN_DIR)/segv

RM := rm -rf

.PHONY: all mkbin clean

all: mkbin $(TARGETS)

mkbin:
	@mkdir -p $(BIN_DIR)

$(BIN_DIR)/%: $(SRC_DIR)/%.c
	$(CC) $< -o $@

clean:
	$(RM) $(BIN_DIR)
