FROM mcr.microsoft.com/devcontainers/base:ubuntu


ENV DEBIAN_FRONTEND=noninteractive


# Native tools we'll use in later steps; safe to install now
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr tesseract-ocr-eng \
    ghostscript \
    poppler-utils \
    libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Working directory for generated files
RUN mkdir -p /workspaces/.data && chown -R vscode:vscode /workspaces/.data