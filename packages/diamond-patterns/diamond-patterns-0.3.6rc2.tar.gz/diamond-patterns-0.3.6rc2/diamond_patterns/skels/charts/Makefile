CHARTS = \
	file1.png

MERMAID = ~/node_modules/.bin/mmdc

all: $(CHARTS)
	cp *.png ../presentation/images/charts
	@echo done

%.png: %.mmd
	@echo compiling $<...
	$(MERMAID) -i "$(basename $<).mmd" -o $(basename $<).png
