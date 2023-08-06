pdf:
	pandoc -f markdown -t beamer --include-in-header preamble.tex -V theme=Madrid -V colortheme=seagull -o presentation.pdf presentation.md

tex:
	pandoc -f markdown -t beamer --include-in-header preamble.tex -V theme=Madrid -V colortheme=seagull -o presentation.tex presentation.md

all: pdf
	cp presentation.pdf ../products
	@echo "Done"

.PHONY: all pdf
