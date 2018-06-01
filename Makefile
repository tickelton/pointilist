SRCDIR = pointilist
TESTDIR = tests
TEST_PY = $(wildcard $(TESTDIR)/*.py)

.PHONY: test

all: test

test:
	@python -m unittest discover $(TESTDIR)

lint:
	@pylint $(SRCDIR)

style:
	@pycodestyle $(SRCDIR)

testlint:
	@pylint $(TEST_PY)

teststyle:
	@pycodestyle $(TESTDIR)
