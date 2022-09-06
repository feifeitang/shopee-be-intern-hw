.PHONY: venv-activate
venv-activate:
	@source env/bin/activate

.PHONY: freeze-reqs
freeze-reqs:
	@python3 -m pip freeze > requirements.txt

.PHONY: install-pkgs
install-pkgs:
	@python3 -m pip install requests

.PHONY: start-worker
start-worker:
	@celery -A tasks worker --loglevel=info

.PHONY: dev
dev:
	@flask --app main --debug run