FROM ubuntu
ADD . /ticket
WORKDIR /ticket
RUN apt-get update
RUN export LANG=zh_CN.UTF-8
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN apt install chromium-browser -y
RUN apt install chromium-chromedriver -y
RUN pip3 install -r requirements.txt

CMD ["python3", "app.py"]