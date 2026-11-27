FROM python:3.13-slim

# uv for fast, lockfile-exact installs
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first so this layer is cached between code changes
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked --no-dev --no-install-project

COPY . .

# Run as an unprivileged user; only the sandbox folder is writable
RUN useradd --uid 1000 --no-create-home --shell /usr/sbin/nologin agent \
    && chown -R agent:agent /app/calculator
USER agent

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["python", "main.py"]
