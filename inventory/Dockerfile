FROM python:3.12-slim
WORKDIR /app
COPY app.py .
# Flush logs immediately so `kubectl logs` shows them in real time
ENV PYTHONUNBUFFERED=1
# TODO: add the instruction that documents which port the container listens on
CMD ["python", "app.py"]
