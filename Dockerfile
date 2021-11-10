FROM python:3.10-slim-buster as builder

WORKDIR /app

RUN python -m venv .venv && .venv/bin/pip install --no-cache-dir -U pip setuptools

COPY requirements.txt .

RUN .venv/bin/pip install --no-cache-dir -r requirements.txt && find /app/.venv \( -type d -a -name test -o -name tests \) -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) -exec rm -rf '{}' \+

FROM python:3.10-slim-buster

RUN useradd -m debian
WORKDIR /home/debian/app

COPY --from=builder /app /home/debian/app

COPY services/ services/
COPY announcement_scraper.py load_config.py logger.py ./

ENV PATH="/home/debian/app/.venv/bin:$PATH"

USER debian

CMD [ "tail", "-f", "/dev/null" ]
