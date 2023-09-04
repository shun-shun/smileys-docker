FROM python:3.9-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /src
COPY api ./

RUN pip install -r requirements.txt


ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]