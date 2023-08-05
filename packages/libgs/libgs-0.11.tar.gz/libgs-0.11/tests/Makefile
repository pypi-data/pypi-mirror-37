#
# Simple makefile to run unit tests and generate html reports
#

BUILDDIR				= build
SOURCEDIR   		= source
SPHINXTARGETDIR = ../doc/source/_static/
HTMLREPFILE			= report.html
COVREPDIR				= covrep
PYTEST					= pytest
COVMODULE				= adfags


#
pytest:
	@echo "Running pytest and creating reports"

	@$(PYTEST) --cov-report "html:$(BUILDDIR)/$(COVREPDIR)" --cov="$(COVMODULE)" \
		--html="$(BUILDDIR)/$(HTMLREPFILE)" --self-contained-html

copy2sphinx:
	@cp  "$(SOURCEDIR)"



.DEFAULT:
	@echo caught target $@
