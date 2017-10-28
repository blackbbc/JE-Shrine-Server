### User

| field        | type     | remark |
| ------------ | -------- | -----  |
| _id          | ObjectId |        |
| username     | string   |        |
| passwordHash | string   |        |
| email        | string   |        |
| role         | int      |        |
| avatar       | string   |        |

### Tag

| field        | type     | remark |
| ------------ | -------- | -----  |
| _id          | ObjectId |        |
| name         | string   |        |

### Music

| field        | type     | remark |
| ------------ | -------- | -----  |
| _id          | ObjectId |        |
| title        | string   |        |
| alias        | [string] |        |
| userId       | ObjectId |        |
| author       | string   |        |
| album        | string   |        |
| tags         | [string] |        |
| content      | string   |        |
| createDt     | Datetime |        |
| updateDt     | Datetime |        |
| images       | dict     | {"small": string, "large": string} |
| references   | dict     | [{"name": string, "url": string}]  |
| views        | int      |        |
| status       | int      |        |

### Star

| field        | type       | remark |
| ------------ | ---------- | -----  |
| _id          | ObjectId   |        |
| userId       | ObjectId   |        |
| name         | string     |        |
| music        | [ObjectId] |        |
| createDt     | Datetime   |        |
| updateDt     | Datetime   |        |

### Feedback

| field        | type     | remark |
| ------------ | -------- | -----  |
| _id          | ObjectId |        |
| musicId      | ObjectId |        |
| email        | string   |        |
| content      | string   |        |
| createDt     | Datetime |        |
