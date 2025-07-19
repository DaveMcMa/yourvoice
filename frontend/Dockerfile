FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY logo.png .

RUN useradd -m -u 1000 gradio && chown -R gradio:gradio /app
USER gradio

EXPOSE 7860

ENV TTS_API_URL=""
ENV TTS_API_TOKEN=""

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:7860/ || exit 1

CMD ["python", "app.py"]