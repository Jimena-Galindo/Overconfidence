# install missing packages from the lockfile
renv::restore()

# paper options
knitr::opts_chunk$set(eval=T, echo=F, warning=F, message=F, cache=F)

# compile the paper
rmarkdown::render("Paper/draft.Rmd", output_format = "pdf_document")

rmarkdown::render("Paper/Intro.Rmd", output_format = "pdf_document")



