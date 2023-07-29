FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /home/app
ENV PROMETHEUS_MULTIPROC_DIR=/multiproc_dir

WORKDIR /home/app

COPY ./pyproject.toml ./poetry.lock* ./

RUN pip install poetry
RUN poetry install
RUN mkdir -p $PROMETHEUS_MULTIPROC_DIR

COPY . ./

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]