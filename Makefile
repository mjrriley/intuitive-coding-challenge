init:
	@python3 -m pip install -r requirements.txt .

test:
	@python3 test/python_binding_test.py
	@python3 test/application_test.py

style:
	@pycodestyle --show-source test/python_binding_test.py app/application.py\
		&& echo "Success: PEP8 Compliant"\
		|| echo "Failed: PEP8 Non-compliant"

clean:
	@rm -rf build
	@rm -rf *.egg-info

.PHONY: init test style clean
