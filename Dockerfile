FROM debian:buster-slim

COPY dist/asgard /usr/local/bin/asgard
RUN set -eux; \
    chmod +x /usr/local/bin/asgard; \
    apt-get update; apt-get install -y --no-install-recommends \
    ca-certificates \
    git \
    openssh-client \
    ; \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT [ "/usr/local/bin/asgard" ]
CMD [ "--help" ]
