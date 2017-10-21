# API文档

## 用户相关

### POST /login
登录

username: string
password: string

### GET /logout
注销

### POST /register
注册

username: string
email: string
password: string
password2: string

### GET /users
获取所有人的信息，需要Admin权限
page: int
size: int

### GET /users/ID
获取个人信息，需要权限

### PUT /users/ID
更新个人信息，需要权限

## 歌曲相关

### GET /music
获取歌曲列表

page: int
size: int
order: string [asc|desc]
sort: string [date|hot]

### POST /music
创建歌曲，需要Admin或者VIP权限


### GET /music/ID
获取歌曲详情


### PUT /music/ID
更新歌曲，需要Admin或者VIP权限


### AJAX GET /search
获取搜索候选项

keyword: string


### POST /search
搜索歌曲

keyword: string
page: int
size: int
