init:
	@python3 -m pip install -r requirements.txt .

test:
	@python3 -m unittest

style:
	@pycodestyle --show-source \
		test/*.py \
		app/*.py \
		&& echo "Success: PEP8 Compliant"\
		|| echo "Failed: PEP8 Non-compliant"

clean:
	@rm -rf build
	@rm -rf *.egg-info
	@rm -rf app/__pycache__
	@rm -rf test/__pycache__

.PHONY: init test style clean
