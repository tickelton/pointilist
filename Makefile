SRCDIR = pointilist
TESTDIR = tests

.PHONY: test

all: test

test:
	@python -m unittest discover $(TESTDIR)

lint:
	@pylint $(SRCDIR)

style:
	@pycodestyle $(SRCDIR)
