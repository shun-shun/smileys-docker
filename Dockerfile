FROM python:3.9-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /src
COPY api ./

RUN pip3 install --upgrade pip && \
    pip3 install fastapi && \
    pip3 install "uvicorn[standard]" && \
    pip3 install requests && \
    pip3 install py-feat && \
    pip install python-multipart


ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]