# bookdown tufte

all: clean html pdf
	@echo "Done"

html:
	Rscript -e "library(bookdown); bookdown::render_book('article.Rmd', 'bookdown::tufte_html2')"
	mkdir -p docs
	mv index.html docs

pdf:
	Rscript -e "library(bookdown); bookdown::render_book('article.Rmd', 'bookdown::pdf_book')"

clean:
	rm -rf docs && mkdir docs
	rm -f index.html
	rm -rf _bookdown_files/
	@echo "Clean"

depends:
	Rscript -e "install.packages(c('bookdown', 'lubridate', 'RColorBrewer', 'ggplot2', 'tufte', 'knitr'), repos='http://cran.us.r-project.org')"

.PHONY: clean depends html pdf all
