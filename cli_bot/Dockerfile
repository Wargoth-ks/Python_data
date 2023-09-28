# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11.5-slim-bookworm

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1


#ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_VIRTUALENVS_CREATE=0

ARG USERNAME=Xuser
ARG APP=cli_bot

RUN pip install -U pip setuptools \
    && pip install poetry \
    && useradd -m -G users $USERNAME \
    && poetry config virtualenvs.path --unset

WORKDIR /home/$USERNAME/$APP

COPY pyproject.toml poetry.lock ./

# Install pip requirements
RUN poetry check

COPY . .

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers

RUN poetry install --no-interaction --no-cache \
    && poetry config virtualenvs.in-project true \
    && chown -R $USERNAME:users /home/$USERNAME

USER $USERNAME

WORKDIR /home/$USERNAME/$APP/$APP

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["poetry", "run", "python", "main.py"]
