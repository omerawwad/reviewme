# Review Me

Review Me is website where you can add review about anything you wan't to contribute by your opinion about, whatever its a product, place, service or any other thing. You can also add reviews in fully anonymous way without showing your Identity. The website is made to help people search about products, places, services, ... taking in consideration previous people experiences in a fully freedom oriented platform.

## Technologies and Implementation

### **[Backend](#Backend)**

I **designed and Implemented over 30 RESTful APIs** with different roles and authorization. The backend is implemented using **Python** with **Django** and the database stored using containerized **Postgres** with **Docker**.

### **[Frontend](#Frontend)**

The frontend is designed and implemented using **React** applying React best practices using **States**, **Props**, **React Router**, **Hooks**, ... that communicate to the backend using RESTful APIs.

## Backend

### ORM and Database

The Database schema is set to have <strong>11 Tables</strong> to insure the system features and here there are.

![review me database schema](./images/reviewme-schema.png)

### API and Backend Endpoints

The backend is designed to produce **20** RESTful API endpoints with handling different scenarios of success and failure.

| **Method** | **Endpoint**              | **Sucess**                | **Failure**       | **Level** | param                         |
| ---------- | ------------------------- | ------------------------- | ----------------- | --------- | ----------------------------- |
| `GET`      | `/items`                  | `200 OK` `page<Item>`     | `404 NOT FOUND`   | Guest     | `page` `size` `sort`          |
| GET        | `/item/{item_id}`         | `200 OK` `Item`           | `404 NOT FOUND`   | Guest     | `item_id`                     |
| GET        | `/review/{review_id}`     | `200 OK` `Review`         | `404 NOT FOUND`   | Guest     | `review_id`                   |
| GET        | `/question/{question_id}` | `200 OK` `Question`       | `404 NOT FOUND`   | Guest     | `question_id`                 |
| GET        | `/user/reviews`           | `200 OK` `List<Review>`   | `404 NOT FOUND`   | Guest     | -                             |
| GET        | `/user/questions`         | `200 OK` `List<Question>` | `404 NOT FOUND`   | Guest     | -                             |
| GET        | `/user/answers`           | `200 OK` `List<Answer>`   | `404 NOT FOUND`   | Guest     | -                             |
| POST       | `/item`                   | `201 Created`             | `400 BAD REQUEST` | Auth      | `item`                        |
| POST       | `/tag`                    | `201 Created`             | `400 BAD REQUEST` | Auth      | `item_id`, `tag_name`         |
| POST       | `/review`                 | `201 Created`             | `400 BAD REQUEST` | Auth      | `review`                      |
| POST       | `/question`               | `201 Created`             | `400 BAD REQUEST` | Auth      | `question`                    |
| POST       | `/answer`                 | `201 Created`             | `400 BAD REQUEST` | Auth      | `question_id`, `answer_text`  |
| POST       | `/like/review`            | `201 CREATED`             | `400 BAD REQUEST` | Auth      | `review_id`                   |
| POST       | `/upvote/question`        | `201 CREATED`             | `400 BAD REQUEST` | Auth      | `question_id`                 |
| POST       | `/like/answer`            | `201 CREATED`             | `400 BAD REQUEST` | Auth      | `answer_id`                   |
| PUT        | `/edit/item`              | `200 OK` `Item`           | `400 BAD REQUEST` | Auth      | `item_id`, `fields to update` |
| PUT        | `/remove/tag`             | `204 NO CONTENT`          | `400 BAD REQUEST` | Auth      | `item_id`, `tag_name`         |
| DELETE     | `/delete/item`            | `204 NO CONTENT`          | `404 NOT FOUND`   | Auth      | `item_id`                     |
| DELETE     | `/delete/review`          | `204 NO CONTENT`          | `404 NOT FOUND`   | Auth      | `review_id`                   |
| DELETE     | `/delete/question`        | `204 NO CONTENT`          | `404 NOT FOUND`   | Auth      | `question_id`                 |
| DELETE     | `/delete/answer`          | `204 NO CONTENT`          | `404 NOT FOUND`   | Auth      | `answer_id`                   |
| DELETE     | `/delete/media`           | `204 NO CONTENT`          | `404 NOT FOUND`   | Auth      | `media_id`                    |
| DELETE     | `/delete/link`            | `204 NO CONTENT`          | `404 NOT FOUND`   | Auth      | `link_id`                     |
| DELETE     | `/unlike/review`          | `204 NO CONTENT`          | `400 BAD REQUEST` | Auth      | `review_id`                   |
| DELETE     | `/unlike/answer`          | `204 NO CONTENT`          | `400 BAD REQUEST` | Auth      | `answer_id`                   |
| DELETE     | `/unupvote/question`      | `204 NO CONTENT`          | `400 BAD REQUEST` | Auth      | `question_id`                 |
