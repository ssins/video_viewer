FROM python:3.7.1

# 设置时区
ENV TZ Asia/Shanghai

WORKDIR /usr/src/app

#更新apt-get源
RUN set -eux; \
    mv /etc/apt/sources.list /etc/apt/sources.list.bak; \
    echo "deb http://mirrors.ustc.edu.cn/debian/ buster main non-free contrib" >/etc/apt/sources.list; \
    echo "deb http://mirrors.ustc.edu.cn/debian/ buster-proposed-updates main non-free contrib" >>/etc/apt/sources.list; \
    echo "deb-src http://mirrors.ustc.edu.cn/debian/ buster main non-free contrib" >>/etc/apt/sources.list; \
    echo "deb-src http://mirrors.ustc.edu.cn/debian/ buster-proposed-updates main non-free contrib" >>/etc/apt/sources.list; \
    apt update; \
    apt-get -y install tzdata; \
    apt-get -y install zbar-tools; \
    ln -sf /usr/share/zoneinfo/${TZ} /etc/localtime; \
    echo "${TZ}" > /etc/timezone;

COPY requirements.txt ./
    
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

COPY . .

CMD ["gunicorn", "server:app", "-c", "./gunicorn.conf.py"]