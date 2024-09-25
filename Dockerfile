# 使用官方 Python 基础镜像
FROM python:3.9.19

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器中
COPY . /app

# 安装项目依赖
RUN pip install fastapi uvicorn pydantic requests typing

# 暴露容器的端口
EXPOSE 8000

# 指定运行uvicorn命令启动应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]