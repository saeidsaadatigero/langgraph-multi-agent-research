# 🐳 Docker Setup Guide for Iranian Developers

<div align="center">

**راهنمای جامع نصب و راه‌اندازی Docker در ایران — بدون Docker Desktop، بدون تحریم، بدون فیلترشکن**

</div>

---

## 📋 Table of Contents

- [چرا Docker Desktop در ایران کار نمی‌کنه؟](#-چرا-docker-desktop-در-ایران-کار-نمی‌کنه)
- [پیش‌نیازها](#-پیش‌نیازها)
- [مرحله ۱: نصب WSL 2](#-مرحله-۱-نصب-wsl-2)
- [مرحله ۲: نصب اوبونتو داخل WSL](#-مرحله-۲-نصب-اوبونتو-داخل-wsl)
- [مرحله ۳: نصب Docker Engine داخل اوبونتو](#-مرحله-۳-نصب-docker-engine-داخل-اوبونتو)
- [مرحله ۴: راه‌اندازی Docker Daemon](#-مرحله-۴-راه‌اندازی-docker-daemon)
- [مرحله ۵: رفع مشکل DNS](#-مرحله-۵-رفع-مشکل-dns)
- [مرحله ۶: Dockerfile استاندارد برای پروژه‌های پایتون](#-مرحله-۶-dockerfile-استاندارد-برای-پروژه‌های-پایتون)
- [مرحله ۷: بیلد و اجرا](#-مرحله-۷-بیلد-و-اجرا)
- [مرحله ۸: docker-compose.yml](#-مرحله-۸-docker-composeyml)
- [مرحله ۹: اسکریپت خودکار اجرا](#-مرحله-۹-اسکریپت-خودکار-اجرا)
- [دستورات پرکاربرد Docker](#-دستورات-پرکاربرد-docker)
- [Troubleshooting](#-troubleshooting)
- [Checklist نهایی](#-checklist-نهایی)

---

## ❓ چرا Docker Desktop در ایران کار نمی‌کنه؟

| مشکل | دلیل | راه‌حل |
|------|------|--------|
| لاگین نمی‌شه | تحریم — Docker Inc. کاربرای ایرانی رو بلاک کرده | بدون لاگین استفاده کن |
| آیکون زرد می‌مونه | Docker Engine نمی‌تونه راه بیفته | از Docker Engine داخل WSL استفاده کن |
| دانلود نشدن imageها | DNS فیلتره | از `--dns 8.8.8.8` استفاده کن |
| error: iptables | WSL کرنل nftables نداره | `--iptables=false` |

**نتیجه:** Docker Desktop رو کلاً بی‌خیال شو. Docker Engine داخل WSL 2 ازش بهتره و بدون هیچ مشکلی کار می‌کنه.

---

## ✅ پیش‌نیازها

- **Windows 10/11 (64-bit)**
- **PowerShell 5.1 یا بالاتر** (Windows PowerShell یا PowerShell 7)
- **اتصال اینترنت** (برای دانلود اولیه)
- **8GB RAM** (توصیه می‌شه)
- **VPN** (برای بعضی از دانلودها — نه برای اجرا)

---

## 🪟 مرحله ۱: نصب WSL 2

### ۱.۱: PowerShell رو **Administrator** باز کن

روی Start کلیک کن → تایپ کن `PowerShell` → راست‌کلیک → **Run as Administrator**

### ۱.۲: WSL رو نصب کن

```powershell
wsl --install
```

اگه ارور داد، دستی نصب کن:

```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

سیستم رو **restart** کن.

### ۱.۳: WSL 2 رو به عنوان پیش‌فرض تنظیم کن

```powershell
wsl --set-default-version 2
```

---

## 🐧 مرحله ۲: نصب اوبونتو داخل WSL

### ۲.۱: نصب کن

```powershell
wsl --install -d Ubuntu
```

صبر کن دانلود و نصب بشه. یه ترمینال جدید باز می‌شه که username و password می‌خواد:

- **Username:** `saeid` (هر چی دوست داری)
- **Password:** یه رمز ساده مثل `admin123` (تایپ می‌کنی ولی نشون داده نمی‌شه)

### ۲.۲: اگه Microsoft Store فیلتر بود

فایل wsl رو دستی دانلود و import کن:

```powershell
# دانلود (با VPN)
wsl --install -d Ubuntu --web-download

# یا import دستی
wsl --import Ubuntu D:\WSL\Ubuntu ubuntu-24.04-wsl-amd64.wsl --version 2
```

### ۲.۳: ورژن WSL رو چک کن

توی **PowerShell ویندوز** (نه داخل WSL):

```powershell
wsl --list --verbose
```

باید ببینی Ubuntu با Version 2 هست:

```
  NAME      STATE           VERSION
* Ubuntu    Running         2
```

### ۲.۴: وارد WSL بشو

```powershell
wsl
```

حالا باید توی ترمینال اوبونتو باشی. prompt باید شبیه این باشه:

```
saeid@DESKTOP:~$
```

اگه `root@DESKTOP` بودی، یه کاربر معمولی بساز:

```bash
useradd -m -s /bin/bash saeid
passwd saeid
usermod -aG sudo saeid
exit
```

بعد دوباره با کاربر جدید وارد شو:

```powershell
wsl -d Ubuntu --user saeid
```

---

## 🐳 مرحله ۳: نصب Docker Engine داخل اوبونتو

این دستورات رو **داخل WSL (اوبونتو)** بزن، نه PowerShell:

```bash
# آپدیت پکیج‌ها
sudo apt update && sudo apt upgrade -y

# نصب Docker Engine
sudo apt install docker.io -y

# چک کن نصب شده
docker --version
```

باید ببینی: `Docker version 29.x.x`

---

## 🟢 مرحله ۴: راه‌اندازی Docker Daemon

### ۴.۱: تنظیم iptables به legacy (برای WSL)

```bash
sudo update-alternatives --set iptables /usr/sbin/iptables-legacy
sudo update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy
```

### ۴.۲: اجرای Docker Daemon

```bash
sudo dockerd --iptables=false --dns 8.8.8.8 --dns 8.8.4.4 &
sleep 3
```

### ۴.۳: تست کن Docker راه افتاده

```bash
sudo docker ps
sudo docker run hello-world
```

باید `Hello from Docker!` رو ببینی.

### ۴.۴: خودکار راه‌اندازی بشه (اختیاری)

اینو به `~/.bashrc` اضافه کن تا هر بار WSL رو باز می‌کنی، Docker خودکار راه بیفته:

```bash
echo '' >> ~/.bashrc
echo '# Auto-start Docker daemon (WSL workaround)' >> ~/.bashrc
echo 'if ! sudo docker ps > /dev/null 2>&1; then' >> ~/.bashrc
echo '    echo "🐳 Starting Docker..."' >> ~/.bashrc
echo '    sudo dockerd --iptables=false --dns 8.8.8.8 --dns 8.8.4.4 > /dev/null 2>&1 &' >> ~/.bashrc
echo '    sleep 2' >> ~/.bashrc
echo 'fi' >> ~/.bashrc
```

---

## 🔧 مرحله ۵: رفع مشکل DNS

**مشکل:** داخل کانتینر، `pip install` و `apt-get` با ارور `Temporary failure resolving` مواجه می‌شن.

**راه‌حل:** همیشه از `--network=host` و `--dns 8.8.8.8` استفاده کن.

```bash
# موقع بیلد
sudo docker build --network=host -t my-app:latest .

# موقع اجرا
sudo docker run -it --rm --network=host my-app:latest
```

**چرا `--network=host`؟** DNS کانتینر مستقیم به DNS host وصل می‌شه و مشکل resolve حل می‌شه.

---

## 📦 مرحله ۶: Dockerfile استاندارد برای پروژه‌های پایتون

این یه Dockerfile استاندارد برای پروژه‌های پایتونیه. کپی کن توی ریشهٔ پروژه‌ت:

```dockerfile
# Dockerfile
# Standard Dockerfile for Python projects

FROM python:3.12-slim

# ── Metadata ────────────────────────────────────
LABEL maintainer="Saeid Saadatigero <saeidsaadatigero@gmail.com>"
LABEL version="1.0.0"

# ── Environment ─────────────────────────────────
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV APP_HOME=/app
WORKDIR $APP_HOME

# ── Dependencies ────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Application ─────────────────────────────────
COPY src/ ./src/
COPY main.py .
COPY .env.example .

# ── Security ────────────────────────────────────
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser $APP_HOME
USER appuser

# ── Entry Point ─────────────────────────────────
CMD ["python", "main.py"]
```

**نکات مهم:**
- `FROM python:3.12-slim` — ایمیج سبک (فقط ۱۵۰MB)
- `--no-cache-dir` — حجم image رو کم می‌کنه
- `USER appuser` — امنیت (root اجرا نمی‌شه)
- **حتماً `.env` واقعی رو توی image کپی نکن!** فقط `.env.example` کپی می‌شه

---

## 🚀 مرحله ۷: بیلد و اجرا

### ۷.۱: فایل `.env` رو بساز

```bash
# توی WSL
cd /mnt/d/projects/my-project
nano .env
```

مقادیر API Key و تنظیمات رو وارد کن. Ctrl+O → Enter → Ctrl+X

### ۷.۲: بیلد

```bash
sudo docker build --network=host -t my-app:latest .
```

### ۷.۳: اجرا

```bash
sudo docker run -it --rm --network=host --env-file .env my-app:latest
```

**فلگ‌های مهم:**
| فلگ | معنی |
|------|------|
| `-it` | Interactive — می‌تونی ورودی بدی |
| `--rm` | بعد از خروج، کانتینر پاک بشه |
| `--network=host` | رفع مشکل DNS در ایران |
| `--env-file .env` | API Keyها رو از فایل .env می‌خونه |
| `my-app:latest` | اسم image که build کردی |

---

## 🎼 مرحله ۸: docker-compose.yml

این فایل برای پروژه‌های چند-کانتینره (مثل Django + Redis + Celery):

```yaml
# docker-compose.yml
version: "3.9"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      network: host  # مهم برای ایران!
    image: my-app:latest
    container_name: my-app-container
    stdin_open: true
    tty: true
    env_file:
      - .env
    volumes:
      - ./src:/app/src:ro
      - ./main.py:/app/main.py:ro
    restart: "no"
    network_mode: host  # مهم برای ایران!

  # redis:
  #   image: redis:7-alpine
  #   container_name: my-app-redis
  #   network_mode: host

  # celery:
  #   build: .
  #   command: celery -A config worker -l info
  #   env_file:
  #     - .env
  #   network_mode: host
```

---

## 📜 مرحله ۹: اسکریپت خودکار اجرا

فایل `run_docker.sh` رو توی ریشهٔ پروژه بساز:

```bash
#!/bin/bash
# run_docker.sh — Quick launcher for Docker projects (WSL 2)
# Usage: ./run_docker.sh

echo "🐳 Starting Docker daemon..."
sudo dockerd --iptables=false --dns 8.8.8.8 --dns 8.8.4.4 > /dev/null 2>&1 &
sleep 3

echo "🔍 Checking Docker..."
if ! sudo docker ps > /dev/null 2>&1; then
    echo "❌ Docker failed to start."
    echo "   Try manually: sudo dockerd --iptables=false --dns 8.8.8.8 &"
    exit 1
fi

echo "🐳 Docker is running!"
echo "🚀 Building image..."
sudo docker build --network=host -t my-app:latest .

echo "🚀 Launching application..."
sudo docker run -it --rm --network=host --env-file .env my-app:latest
```

**توی WSL:**

```bash
chmod +x run_docker.sh
./run_docker.sh
```

---

## 📋 دستورات پرکاربرد Docker

| دستور | کاربرد |
|-------|--------|
| `sudo docker ps` | لیست کانتینرهای در حال اجرا |
| `sudo docker ps -a` | همهٔ کانتینرها (حتی خاموش) |
| `sudo docker images` | لیست imageهای دانلود شده |
| `sudo docker build -t name:latest .` | بیلد image جدید |
| `sudo docker run -it --rm name:latest` | اجرای کانتینر |
| `sudo docker stop <id>` | متوقف کردن کانتینر |
| `sudo docker rm <id>` | حذف کانتینر |
| `sudo docker rmi <id>` | حذف image |
| `sudo docker system prune -a` | پاکسازی کامل (همهٔ imageها و کانتینرهای بلااستفاده) |
| `sudo docker logs <id>` | دیدن لاگ کانتینر |
| `sudo docker exec -it <id> bash` | وارد shell کانتینر شدن |

---

## 🩺 Troubleshooting

| ارور | علت | راه‌حل |
|------|------|--------|
| `docker: unrecognized service` | Docker Daemon نصب نیست یا systemd غیرفعاله | `sudo dockerd --iptables=false &` |
| `Cannot connect to the Docker daemon` | Docker Daemon خاموشه | `sudo dockerd --iptables=false --dns 8.8.8.8 &` |
| `Temporary failure resolving 'deb.debian.org'` | DNS کانتینر کار نمی‌کنه | از `--network=host` موقع build و run استفاده کن |
| `Temporary failure in name resolution` (pip) | DNS کانتینر کار نمی‌کنه | از `--network=host` موقع build و run استفاده کن |
| `Error initializing network controller: iptables` | WSL nftables نداره | `--iptables=false` |
| `failed to start daemon: process with PID X is still running` | Docker Daemon قبلی هنوز زنده‌ست | `sudo pkill dockerd` بعد sleep 2 |
| `The command 'docker' could not be found in this WSL 2 distro` | Docker داخل WSL نصب نیست | `sudo apt install docker.io -y` |
| `WSL has no installed distributions` | اوبونتو unregister شده | `wsl --install -d Ubuntu` |

---

## ✅ Checklist نهایی

### نصب اولیه (فقط یه بار)

- [ ] PowerShell Administrator → `wsl --install`
- [ ] Restart ویندوز
- [ ] `wsl --set-default-version 2`
- [ ] `wsl --install -d Ubuntu`
- [ ] داخل WSL: `sudo apt install docker.io -y`
- [ ] `sudo dockerd --iptables=false --dns 8.8.8.8 &`
- [ ] `sudo docker run hello-world` (تست موفقیت‌آمیز)

### برای هر پروژه جدید

- [ ] فایل `Dockerfile` توی ریشهٔ پروژه
- [ ] فایل `.env` با API Keyهای واقعی
- [ ] فایل `.dockerignore` (اختیاری)
- [ ] فایل `docker-compose.yml` (اگه چند سرویس داری)
- [ ] فایل `run_docker.sh` (برای اجرای سریع)
- [ ] `sudo docker build --network=host -t project-name:latest .`
- [ ] `sudo docker run -it --rm --network=host --env-file .env project-name:latest`

### هر بار که WSL رو باز می‌کنی

- [ ] `sudo docker ps` (چک کن Docker زنده‌ست یا نه)
- [ ] اگه ارور `Cannot connect` دادی: `sudo dockerd --iptables=false --dns 8.8.8.8 &`
- [ ] پروژه رو اجرا کن

---

## 🎯 جمع‌بندی

> **Docker Desktop رو فراموش کن. Docker Engine داخل WSL 2 تنها راه پایدار برای توسعه‌دهنده‌های ایرانیه.**

| Docker Desktop ❌ | Docker Engine + WSL 2 ✅ |
|-------------------|--------------------------|
| نیاز به لاگین | بدون لاگین |
| ۴ گیگ رم مصرف | ۲۰۰ مگ رم |
| تحریم روش تأثیر داره | بدون مشکل |
| GUI سنگین | فقط CLI (حرفه‌ای) |
| باگ iptables | با `--iptables=false` حل می‌شه |

---

<div align="center">

**🐳 Built with Docker Engine on WSL 2 — The Iranian Developer's Way**

*"If Docker Desktop doesn't work, go to the source — pure Docker Engine always does."*

</div>
