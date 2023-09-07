FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /strangling_monolith
COPY requirements.txt /strangling_monolith/
RUN pip install -r requirements.txt
COPY . /strangling_monolith/