

FROM python:3.10


WORKDIR /app


COPY . .


RUN pip install --no-cache-dir -r requirements.txt


CMD ["sh", "-c", "python -u inference.py && tail -f /dev/null"]