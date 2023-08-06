# bookdown tufte

all: clean html pdf
	cp _assets/index.html docs
	cp article.html docs
	cp article.pdf docs
	@echo "Done"

html:
	Rscript -e "library(bookdown); bookdown::render_book('article.Rmd', 'bookdown::tufte_html2')"

pdf:
	Rscript -e "library(bookdown); bookdown::render_book('article.Rmd', 'bookdown::pdf_book')"

clean:
	rm -rf docs && mkdir docs
	# rm -f analysis/index.Rmd
	# rm -f analysis/*.md
	# rm -f analysis/*.pdf
	# rm -f analysis/*.html
	# rm -rf analysis/*_files/
	# rm -rf analysis/_bookdown_files/
	# rm -rf analysis/_book/
	@echo "Clean"

depends:
	Rscript -e "install.packages(c('bookdown', 'lubridate', 'RColorBrewer', 'ggplot2', 'tufte', 'knitr'), repos='http://cran.us.r-project.org')"

.PHONY: clean depends html pdf all
