FROM python:3.11-slim
#FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim
WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

COPY ./app /app

EXPOSE 8000
CMD ["bash", "-c", "uvicorn main:app --proxy-headers --host 0.0.0.0 --port 8000 --workers 2"]