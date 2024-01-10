# Based on https://fastapi.tiangolo.com/deployment/docker/#docker-image-with-poetry

######
# 1. Use poetry to generate requirements.txt
FROM python:3.11 as requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

######
# 2. Use git and git lfs to retrieve the huggingface models.
FROM alpine/git:latest as models-stage

RUN git clone https://huggingface.co/BAAI/bge-small-en /models/embedding && \
    git clone https://huggingface.co/StabilityAI/stablelm-tuned-alpha-3b /models/llm
    # If the above model is too large (~14GB), dolly is smaller (~6GB).
    # On my machine, increasing the Docker memory limit to 16GB made things work.
    # git clone https://huggingface.co/databricks/dolly-v2-3b /models/llm

######
# 3. Create the actual image.
FROM python:3.11
WORKDIR /code

# Copy models first, so they are cached.
COPY --from=models-stage /models /models

# Install requirements second, so they're cached.
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Finally, copy in the application code.
COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]