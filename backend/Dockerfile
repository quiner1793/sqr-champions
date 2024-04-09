# Python base image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /backend

# Copy the project files to the working directory
COPY pyproject.toml poetry.lock /backend/

# Install Poetry and dependencies
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

# Copy the rest of the project files to the working directory
COPY . /backend

# Expose the FastAPI port
EXPOSE 8080

# Start the FastAPI server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]