FROM alpine:3.4

RUN apk add --update make python py-pip && \
    pip install --upgrade pip pkgstack

COPY conf/*.yml /tmp/

RUN pkgstack \
    --profile /tmp/dev-packages.yml \
    --profile /tmp/required-packages.yml
