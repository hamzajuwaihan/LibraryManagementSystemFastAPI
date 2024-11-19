# Note: replacement needed
.PHONY: clean
clean:
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -f .coverage

.PHONY: destroy
destroy:
	docker compose down

.PHONY: lint
lint:
	docker compose run --rm replace-domain-service-test sh -c " \
		flake8 . && \
		isort --check --diff . && \
		mypy replace_domain && \
		yamllint ."

.PHONY: run
run:
	docker compose up -d replace-domain-service

.PHONY: test
update database:
	docker compose run --rm replace-domain-service-alembic

.PHONY: coverage
coverage:
	docker compose run --rm replace-domain-service-test sh -c " \
		coverage run -m pytest && \
		coverage report -m "
