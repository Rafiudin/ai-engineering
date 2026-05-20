FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Enable bytecode compilation and python optimizations 
ENV UV_COMPILE_BYTECODE=1
ENV UV_PYTHON_OPTIMIZE=1
ENV UV_LINK_MODE=copy

# set pyton path to include the app directory
ENV PYTHONPATH="/app/src:$PYTHONPATH"

# Copy only dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --frozen

# Copy the rest of the application code
COPY src ./src/

# Set path to use the virtual environment's python
ENV PATH="/app/.venv/bin:$PATH"

# Create a non-root user and set permissions
RUN addgroup --system app && \
    adduser --system --ingroup app app && \
    chown -R app:app /app && \
    mkdir -p /home/app && \
    chown -R app:app /home/app && \
    mkdir -p /home/app/.streamlit && \
    mkdir -p /home/app/.streamlit/data && \
    mkdir -p /home/app/.streamlit/cache && \
    chown -R app:app /home/app/.streamlit

# Set home directory for the app user
ENV HOME=/home/app

# Switch to the non-root user
USER app

# Expose the port that Streamlit will run on
EXPOSE 8501

# Set the entrypoint to run the Streamlit app
CMD ["uv", "run", "streamlit", "run", "src/app.py", "--server.address=0.0.0.0"]