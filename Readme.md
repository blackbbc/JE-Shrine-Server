# 自由神社
自由神社后端

## 相关文档
1. [数据库结构](doc/db.md)
2. [API文档](doc/api.md)

## 环境要求
- Python 3.6+
- Mongo 3.4+

## 安装依赖
```
[sudo] pip install -r requirements.txt
```

## 启动

1. 确保`MongoDB`运行中
2. 修改`src/config.py.default`相关参数并改名为`src/config.py`
3. 运行服务器
```bash
export FLASK_DEBUG=1
export FLASK_APP=app.py
flask run
```
