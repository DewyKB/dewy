# Based on https://fastapi.tiangolo.com/deployment/docker/#docker-image-with-poetry

######
# 1. Use poetry to generate requirements.txt
FROM python:3.11 as requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

######
# 2. Create the actual image.
FROM python:3.11
WORKDIR /code

# Install requirements second, so they're cached.
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Finally, copy in the application code.
COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]