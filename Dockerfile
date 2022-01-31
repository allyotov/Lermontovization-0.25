FROM python:3.9.7-slim-bullseye

WORKDIR /lermontovization

COPY pyproject.toml poetry.lock /lermontovization/

RUN pip install "poetry==1.1.0" && \
 poetry config virtualenvs.create false && poetry install

COPY bot /lermontovization/bot/

COPY lermontovization /lermontovization/lermontovization/

COPY preprod_research /lermontovization/preprod_research/

CMD ["python", "-m", "bot"]