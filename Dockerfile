FROM python:3.10-bullseye

ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# 1. Instalación base del sistema
RUN apt-get update && apt-get install -y \
    bash \
    curl \
    jq \
    unzip \
    wget \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*

# 2. Instalación de Google Chrome (desglosada)
RUN echo "[INFO] Adding Google signing key" \
 && curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-linux-signing-keyring.gpg \
 && echo "[INFO] Adding Chrome repo" \
 && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

RUN echo "[INFO] Updating APT and installing Chrome" \
 && apt-get update \
 && apt-get install -y google-chrome-stable \
 || (echo "[ERROR] Failed to install google-chrome-stable" && exit 1)

# 3. Instalar ChromeDriver
RUN CHROMEDRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && echo "Using chromedriver version: $CHROMEDRIVER_VERSION" \
    && wget https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip -O /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm /tmp/chromedriver.zip

COPY . .

# 4. Instalación de dependencias de Python
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 5. Configuración de ChromeDriver
EXPOSE 80

CMD ["python", "app.py"]
