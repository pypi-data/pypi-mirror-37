# Outline Makefile

help:
	echo "Use 'make scaffold' to get started."

scaffold: presentation article working
	@echo "Done"

presentation:
    mkdir presentation
    cd presentation && diamond --skel beamer scaffold

article:
    mkdir article
    cd article && diamond --skel article scaffold

working:
    mkdir working
    cd working && diamond --skel tufte scaffold

.PHONY: help scaffold presentation article working
