# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./app ./app
COPY ./static ./static
COPY ./templates ./templates
COPY ./requirements.txt ./requirements.txt

# proxies
ENV HTTP_PROXY=http://proxy.cat.com:80
ENV HTTPS_PROXY=http://proxy.cat.com:80
ENV http_proxy=http://proxy.cat.com:80
ENV https_proxy=http://proxy.cat.com:80
ENV NO_PROXY=169.254.169.254,169.254.170.2,localhost,127.0.0.1,cat.com
ENV no_proxy=169.254.169.254,169.254.170.2,localhost,127.0.0.1,cat.com

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

