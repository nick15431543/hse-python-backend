FROM python:3.12

RUN apt-get update && apt-get install -y gcc
RUN python -m pip install --upgrade pip

RUN mkdir src
WORKDIR /src

COPY lecture_2/ ./lecture_2/

RUN ls -la

RUN pip install -r lecture_2/hw/shop_api/requirements.txt

EXPOSE 8080
CMD ["uvicorn", "lecture_2.hw.shop_api.main:app", "--port", "8080", "--host", "0.0.0.0"]