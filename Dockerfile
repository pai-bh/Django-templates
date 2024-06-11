# Stage 1: Build Stage
FROM python:3.11 AS builder

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy only the dependency files to leverage Docker cache
COPY pyproject.toml ./

# Configure Poetry
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --without dev

# Stage 2: Final Stage
FROM python:3.11-slim

WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local /usr/local

# Copy the application files : 추가로 복사할 것들은 입력 (불필요한 파일 복사를 배제하기 위함)
COPY pyproject.toml README.md manage.py ./
COPY static/ static/
COPY common/ common/
COPY apps/ apps/
# TODO : 프로젝트 명 등 추가할 것

# migrate
RUN python manage.py migrate --noinput

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Entry point
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "{Django프로젝트명}.wsgi:application"]
# ENTRYPOINT ["python", "manage.py","runserver", "0.0.0.0:8000"]