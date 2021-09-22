FROM python:3

RUN pip install matrix-nio
WORKDIR /app
COPY main.py /app
RUN chmod +x /app/main.py

ENTRYPOINT ["/usr/local/bin/python", "main.py"]
