FROM python:3.10-slim

WORKDIR /app

# Copy all project files
COPY . /app

# ✅ Create and activate virtual environment, install Python deps
RUN python3 -m venv /opt/venv \
    && . /opt/venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# ✅ Set the virtualenv as default for all future commands
ENV PATH="/opt/venv/bin:$PATH"

# ✅ Set default command to run your bot
CMD ["python", "handlers/bot.py"]
