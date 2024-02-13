# Based on https://fastapi.tiangolo.com/deployment/docker/#docker-image-with-poetry

######
# 1. Use poetry to generate requirements.txt
FROM python:3.11 as requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

######
# 2. Compile the frontend
FROM node:20.9.0-alpine as frontend-stage
WORKDIR /app
COPY ./dewy/frontend/package.json ./package.json
RUN npm install --silent

COPY ./dewy/frontend/ ./
RUN npm run build

######
# 3. Create the actual image.
FROM python:3.11
WORKDIR /code

# Install requirements second, so they're cached.
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Finally, copy in the application code.
COPY ./dewy /code/dewy
COPY --from=frontend-stage /app/dist /code/dewy/frontend/dist

CMD ["uvicorn", "--factory", "dewy.main:create_app", "--host", "0.0.0.0", "--port", "8000"]