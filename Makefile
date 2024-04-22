clean-pycache:
	find ./ -type d -name '__pycache__' -exec rm -rf {} +

lint:
	poetry run ruff check src/* --fix
	poetry run ruff check utils/* --fix
	poetry run ruff check llama3/serve.py --fix

format:
	poetry run ruff format src/*
	poetry run ruff format utils/*
	poetry run ruff format llama3/serve.py

imports:
	poetry run ruff check src/* --select I --fix
	poetry run ruff check utils/* --select I --fix
	poetry run ruff check llama3/serve.py --select I --fix

pretty:
	$(MAKE) lint
	$(MAKE) format
	$(MAKE) imports

llama8-ct:
	poetry run python utils/download_from_hf.py \
		--repo_id meta-llama/Meta-Llama-3-8B-Instruct \
		--filename tokenizer_config.json \
		--output_file llama3/chat_template.jinja

llama70-ct:
	poetry run python utils/download_from_hf.py \
		--repo_id meta-llama/Meta-Llama-3-70B-Instruct \
		--filename tokenizer_config.json \
		--output_file llama3/chat_template.jinja

serve-llama8:
	$(MAKE) llama8-ct
	poetry run modal serve llama3/serve.py

serve-llama70:
	$(MAKE) llama70-ct
	poetry run modal serve llama3/serve.py

deploy-llama8:
	$(MAKE) llama8-ct
	poetry run modal deploy llama3/serve.py

deploy-llama70:
	$(MAKE) llama70-ct
	poetry run modal deploy llama3/serve.py