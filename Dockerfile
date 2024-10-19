FROM python:3.9

EXPOSE 5002

WORKDIR /authApi

COPY . /authApi/

RUN pip install pipenv && pipenv install

ENV PYTHONPATH /authApi

ENTRYPOINT ["pipenv", "run", "python", "./src/main.py"]