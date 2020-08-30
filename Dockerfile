FROM python:3.6

# prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

WORKDIR /MoviesSite

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /MoviesSite/