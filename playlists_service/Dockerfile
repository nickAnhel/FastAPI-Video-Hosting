FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /project

COPY pyproject.toml ./
RUN python -m pip install --no-cache-dir poetry==1.7.1 \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . .
RUN python -m grpc_tools.protoc -I ./proto --python_out=./app/grpc_transport --pyi_out=./app/grpc_transport --grpc_python_out=./app/grpc_transport ./proto/playlist.proto