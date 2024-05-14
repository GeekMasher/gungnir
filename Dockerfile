FROM python:3.11-alpine

# install syft
RUN apk add bash curl && \
    curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin && \
    rm -rf /var/cache/apk/*

WORKDIR /app

COPY gungnir gungnir

# deps
COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv && \
    pipenv sync --system

# entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod 755 /app/entrypoint.sh

ENTRYPOINT [ "/bin/bash" ]
CMD [ "/app/entrypoint.sh", "setup" ]

