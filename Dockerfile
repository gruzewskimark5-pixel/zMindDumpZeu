FROM python:3.11-slim

WORKDIR /app

# Create a non-root user and group
RUN groupadd -r zpulse && useradd -r -g zpulse zpulse && \
    chown zpulse:zpulse /app

COPY --chown=zpulse:zpulse src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=zpulse:zpulse src/ src/

# Set Python path so src modules can be imported
ENV PYTHONPATH=/app/src

# Switch to the non-root user
USER zpulse

CMD ["python", "src/eventbus.py"]
