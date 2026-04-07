
FROM python:3.10


WORKDIR /app


COPY . .


<<<<<<< HEAD
RUN pip install --no-cache-dir pydantic
=======
RUN pip install --no-cache-dir -r requirements.txt
>>>>>>> 526732f58bda7f94c31854b5b0d982d066fef435


CMD ["python", "inference.py"]