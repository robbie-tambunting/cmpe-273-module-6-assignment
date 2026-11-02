FROM python:3.12-slim
WORKDIR /app
COPY app.py .
# Flush logs immediately so `kubectl logs` shows them in real time
ENV PYTHONUNBUFFERED=1
EXPOSE 8080
CMD ["python", "app.py"]
