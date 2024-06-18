FROM python:3.11.6 as server
RUN curl -fsSL -o /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/latest/download/dbmate-linux-amd64 && \
    chmod +x /usr/local/bin/dbmate
RUN pip install --no-cache-dir --upgrade pip
WORKDIR /project
COPY /requirements/requirements.txt /project/requirements.txt
RUN pip install --no-cache-dir --no-deps --upgrade -r /project/requirements.txt
RUN pip install --upgrade pip
RUN pip install fastembed
COPY . /project
CMD ["bash", "-c", "dbmate up & python -m uvicorn --host 0.0.0.0 --reload app.main:app   "]