FROM python:3.12-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENTRYPOINT ["/bin/sh", "-c", "git config --global user.name '${GIT_USER}' && git config --global user.email '${GIT_EMAIL}' && exec python log_analyze.py \"$@\"", "--"]

#CMD git config --global user.name "${GIT_USER}" && \
#    git config --global user.email "${GIT_EMAIL}" && \
#    python log_analyze.py

#FROM python:3.11
#WORKDIR /app
#COPY . /app
#RUN pip install -r requirements.txt
#ENTRYPOINT ["python", "log_analyze.py"]









