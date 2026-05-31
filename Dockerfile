# Builder stage
FROM python:3.10-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.10-slim
WORKDIR /app

# non-root user setup
COPY --from=builder /root/.local /usr/local
ENV PATH=/usr/local/bin:$PATH
RUN useradd --create-home appuser
COPY . .
RUN chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]