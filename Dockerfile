FROM python:3.11-slim

WORKDIR /app

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/

# Set Python path so src modules can be imported
ENV PYTHONPATH=/app/src

CMD ["python", "src/eventbus.py"]
