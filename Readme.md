![alt](http://www.moeje.org/wp-content/uploads/2016/07/017.jpg)

<p align="center">
  <a href='https://www.versioneye.com/user/projects/598d6f846725bd005228a0e4'><img src='https://www.versioneye.com/user/projects/598d6f846725bd005228a0e4/badge.svg?style=flat-square' alt="Dependency Status" /></a>
  <a href='https://github.com/blackbbc/JE-Shrine-Server/blob/master/LICENSE'><img src='https://img.shields.io/github/license/mashape/apistatus.svg' alt="License" /></a>
</p>

<p align="center">
  <a href="http://www.moeje.org/">自由神社</a>后端部分，使用Flask开发
  前端部分——<a href='https://github.com/TOKdawn/JE_shrine'>https://github.com/TOKdawn/JE_shrine</a>
</p>

## 相关文档
- [数据库结构](doc/db.md)
- [API文档](https://blackbbc.github.io/slate/)

## 环境要求
- Python 3.6+
- Mongo 3.4+
- Elasticsearch 5.0+

## 前置要求

### 安装依赖
```
[sudo] pip install -r requirements.txt
```

### 导入Schema到Elasticsearch中

1. 启动`Elasticsearch`
2. 调用如下API导入Schema
```json
PUT http://localhost:9200/je-shrine

{
    "mappings": {
        "music": {
            "_source": {
                "enabled": true
            },
            "dynamic": false,
            "properties": {
                "title": {"type": "text"},
                "alias": {"type": "text"},
                "author": {"type": "text"},
                "album": {"type": "text"},
                "tags": {"type": "text"},
                "createDt": {"type": "date"},
                "updateDt": {"type": "date"},
                "views": {"type": "integer"}
            }
        }
    }
}
```

## 启动

1. 确保`MongoDB`运行中
2. 确保`Elasticsearch`运行中
3. 启动`mongo-connector`同步`MongoDB`与`Elasticsearch`
```bash
mongo-connector -m localhost:27017 -t localhost:9200 -d elastic2_doc_manager -n je-shrine.music
```
4. 修改`src/config.py.default`相关参数并改名为`src/config.py`
5. 运行服务器
```bash
cd src
export FLASK_DEBUG=1
export FLASK_APP=app.py
flask run
```
