# FastAPI Admin

基于fastapi开发的后台管理系统，适配[Mini Vue Admin](https://gitee.com/front-devops/Mini-Vue-Admin)项目

## 启动
```shell
# 进入项目的app目录
cd app
# 启动项目
python.exe -m uvicorn main:app --reload 
```

## 镜像打包
```shell
docker build -t sanbuliuxin/fastapi-admin:v20240611 .
```

## API文档
Swagger: http://localhost:8000/api/v1/docs