From ubuntu
ADD . /ticket
WORKDIR /work
RUN apt-get update
RUN export LANG=zh_CN.UTF-8
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get install chromium-browser -y
RUN apt-get install chromium-chromedriver -y
RUN pip3 install -r ./requirements.txt

CMD ["python3", "app.py"]