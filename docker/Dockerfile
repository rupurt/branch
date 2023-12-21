# syntax=docker/dockerfile:1.3

FROM python:3.11.6-bookworm AS deps
WORKDIR /app
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY setup.py setup.py
COPY pyproject.toml pyproject.toml
COPY Makefile Makefile
COPY requirements.txt requirements.txt
COPY src src
RUN make deps.install.reqs

FROM python:3.11.6-bookworm AS build
WORKDIR /app
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN apt-get update && apt-get install -y patchelf zlib1g libssl-dev
COPY --from=deps /opt/venv /opt/venv
COPY setup.py setup.py
COPY pyproject.toml pyproject.toml
COPY Makefile Makefile
COPY src src
RUN make build/nuitka

FROM debian:bookworm-20231120-slim AS run
WORKDIR /app
RUN apt-get update && apt-get install -y zlib1g libssl-dev
COPY --from=build /app/nuitka/branch bin/branch
CMD ["/app/bin/branch", "server", "start"]
