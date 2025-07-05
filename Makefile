.PHONY: count

count:
	wc -m input/input.txt

lint:
	rg '[a-zA-Z]' input/input.txt
