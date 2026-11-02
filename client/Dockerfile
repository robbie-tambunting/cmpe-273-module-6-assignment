FROM python:3.12-slim
WORKDIR /app
COPY client.py .
# Flush logs immediately so `kubectl logs -f` shows them in real time
ENV PYTHONUNBUFFERED=1
CMD ["python", "client.py"]
