FROM runpod/base:0.4.0-cuda12.1.0-devel-ubuntu22.04

COPY requirements.txt /requirements.txt
RUN python3 -m pip install -r /requirements.txt

COPY . /app
WORKDIR /app

CMD ["python3", "main.py"]
