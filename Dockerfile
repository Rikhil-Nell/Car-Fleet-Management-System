# Use an official Python 3.12 slim image as the base
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install uv using its official installer script
RUN apt-get update && apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    apt-get purge -y curl && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

# Add uv to the system's PATH environment variable
ENV PATH="/root/.local/bin:$PATH"

# Copy only the dependency files first to leverage Docker's layer caching
COPY pyproject.toml uv.lock ./

# Install project dependencies using the lock file for a fast, reproducible build
RUN uv sync

# Copy the entire backend directory structure
# This preserves the correct structure and includes alembic, etc.
COPY backend/ ./

# Expose the port that the application will run on
EXPOSE 8000

# Define the command to run the application using uv and Uvicorn
# Now the app module is directly accessible at /app/app/main.py
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]