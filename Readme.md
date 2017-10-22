# 自由神社

![alt](http://www.moeje.org/wp-content/uploads/2016/07/017.jpg)

自由神社后端——[http://www.moeje.org/](http://www.moeje.org/)

## 相关文档
- [数据库结构](doc/db.md)
- [API文档](https://blackbbc.github.io/slate/)

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
