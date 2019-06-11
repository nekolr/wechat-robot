FROM python:3.7

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY . .

ENV MODE server

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

ENTRYPOINT ["python", "main.py"]