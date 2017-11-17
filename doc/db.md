### User

| field        | type     | remark   |
| ------------ | -------- | -------- |
| _id          | ObjectId |          |
| bid          | int      | 百度uid  |
| username     | string   |          |
| password     | string   | 密码Hash |
| email        | string   |          |
| role         | int      |          |
| avatar       | string   |          |

### Tag

| field        | type     | remark |
| ------------ | -------- | -----  |
| _id          | ObjectId |        |
| name         | string   |        |

### Music

| field        | type     | remark                             |
| ------------ | -------- | -----                              |
| _id          | ObjectId |                                    |
| title        | string   |                                    |
| alias        | [string] |                                    |
| userId       | ObjectId |                                    |
| author       | string   | 作词                               |
| composer     | string   | 作曲                               |
| singer       | string   | 演唱者                             |
| album        | string   |                                    |
| tags         | [string] |                                    |
| content      | string   | 曲谱内容                           |
| createDt     | datetime |                                    |
| updateDt     | datetime |                                    |
| cover        | string   |                                    |
| references   | dict     | [{"name": string, "url": string}]  |
| views        | int      |                                    |
| status       | int      |                                    |

### Star

| field        | type       | remark |
| ------------ | ---------- | -----  |
| _id          | ObjectId   |        |
| userId       | ObjectId   |        |
| name         | string     |        |
| music        | [ObjectId] |        |
| createDt     | datetime   |        |
| updateDt     | datetime   |        |

### Authorization

| field  | type     | remark |
| ------ | -------- | ------ |
| _id    | ObjectId |        |
| email  | string |        |
| code   | string   |        |
| time   | datetime      |        |

### Feedback

| field        | type     | remark |
| ------------ | -------- | -----  |
| _id          | ObjectId |        |
| musicId      | ObjectId |        |
| email        | string   |        |
| content      | string   |        |
| createDt     | datetime |        |
