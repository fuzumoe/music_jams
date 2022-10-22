# noqa
FROM python:3

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Create directory /code
RUN mkdir /code

# Set working directory to be directory /code
WORKDIR /code

# Laod project python requirements from project artifacts
ADD requirements.txt /code/

# Install project python requirements
RUN pip install -r requirements.txt --no-cache-dir

# Load  applciation artifacts
ADD . /code/

# Run python load static
RUN python manage.py collectstatic --noinput

# Copy docker entrypoint script
ADD docker-entrypoint.sh /usr/local/bin/

# Make sript excutable
RUN chmod u+x /usr/local/bin/docker-entrypoint.sh

# Set docker container pre start script
ENTRYPOINT ["docker-entrypoint.sh"]

# Set start command
CMD ["gunicorn",  "--timeout", "120","--workers","5","--reload", "--bind", "0.0.0.0:8000","music_jam.wsgi"]

# Expose container's port 8000 2222
EXPOSE 8000 2222
