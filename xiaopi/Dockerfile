FROM se1zer/phpstudy:1.29

COPY flag /flag
COPY robot /robot
COPY run.sh /run.sh

RUN sed -i 's@//.*archive.ubuntu.com@//mirrors.ustc.edu.cn@g' /etc/apt/sources.list \
    && apt update \
    && apt install -y python3 python3-pip firefox \
    && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install selenium requests ddddocr \
    && chmod +x /robot/geckodriver /run.sh

ENTRYPOINT ["/bin/sh", "-c", "/run.sh"]