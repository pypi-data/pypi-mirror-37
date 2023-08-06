# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXPROJ    = pypago
SOURCEDIR     = ./source
BUILDDIR      = _build

# User-friendly check for sphinx-build.
ifeq ($(shell which $(SPHINXBUILD) >/dev/null 2>&1; echo $$?), 1)
$(error The '$(SPHINXBUILD)' command was not found. Make sure you have Sphinx installed, then set the SPHINXBUILD environment variable to point to the full path of the '$(SPHINXBUILD)' executable. Alternatively you can add the directory with the executable to your PATH. If you don''t have Sphinx installed, grab it from http://sphinx-doc.org/)
endif

# Has to be explicit, otherwise we don't get "make" without targets right.
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# You can add custom targets here.

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%:

	# Make symbolic links to  make everything work (code inclusion and
	# execution, figure display)
	(cd source/pypago/manual_sources/_static/ && ln -sfv ../../../../figs .)
	(cd source/pypago/manual_sources/_static/ && ln -sfv ../../../../csv .)
	(cd examples && ln -sfv ../figs .)
	(cd examples && ln -sfv ../data .)
	(cd source/pypago/ && ln -sfv ../../examples .)
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: clean
clean:
	rm -rfv _build/*
	rm -rfv ./source/generated
	rm -rfv ./source/pypago/generated
