FROM python:3.8

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY . /home/bot/
WORKDIR /home/bot/
RUN pip install -r requirements.txt

CMD python main.py