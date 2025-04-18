FROM python:3.10-slim

LABEL maintainer="yufeiyohi@outlook.com"
ARG TZ='Asia/Shanghai'

ENV BUILD_PREFIX=/app

ADD . ${BUILD_PREFIX}

RUN apt-get update \
    &&apt-get install -y --no-install-recommends bash vim iputils-ping curl \
    && cd ${BUILD_PREFIX} \
    && /usr/local/bin/python -m pip install --no-cache --upgrade pip \
    && pip install --no-cache -r requirements.txt

# 设置时区
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-6000} --access-logfile - --error-logfile - app:application"]