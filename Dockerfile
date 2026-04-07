

FROM python:3.10


WORKDIR /app


COPY . .


RUN pip install --no-cache-dir -r requirements.txt


<<<<<<< HEAD
CMD ["sh", "-c", "python -u inference.py && tail -f /dev/null"]
=======
CMD ["sh", "-c", "python -u inference.py && tail -f /dev/null"]
>>>>>>> faf9d542a3d131702253473079cafc306939fd28
