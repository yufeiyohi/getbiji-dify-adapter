FROM python:3.10-slim

LABEL maintainer="yufeiyohi@outlook.com"
ARG TZ='Asia/Shanghai'

# 设置时区
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-6000} --access-logfile - --error-logfile - app:app"]