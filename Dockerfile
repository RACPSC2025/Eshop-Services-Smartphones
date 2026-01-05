# Use an official Python runtime as a parent image
FROM python:3.13-slim-bullseye

# Set environment variables to prevent generating .pyc files and to buffer output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install uv, a fast Python package installer
RUN pip install uv

# Copy the dependency files and install dependencies
# Using uv.lock ensures consistent dependencies are installed
COPY uv.lock pyproject.toml ./
RUN uv pip install -p pyproject.toml

# Tailwind CSS
# Install Tailwind CLI
# Ejecutar la descarga del binario de Tailwind CLI
RUN python manage.py tailwind download_cli

# Compilar el CSS para producción (minificado)
RUN python manage.py tailwind build

# Ejecutar collectstatic (esto incluirá el styles.css generado)
RUN python manage.py collectstatic --noinput

# Copy the rest of the application's code into the container
COPY . .

# Expose port 8000 to allow communication with the application
EXPOSE 8000

# Define the command to run the application
# This runs the Django development server. For production, you would use Gunicorn or uWSGI.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
