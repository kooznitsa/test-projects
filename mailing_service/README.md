# Mailing service

## Task description

- Implement methods for creating a new mailout, viewing the created ones, and getting statistics on completed mailouts.
- Implement the service itself for sending notifications to an external API. Design and develop a service that launches a mailout according to a mailing list of customers.

To integrate with the project under development in this task, there is an external service that can receive requests to send messages to customers.

[Original task in Russian](https://www.craft.do/s/n6OVYFVUpq0o6L)

### Mailout logic

- After creating a new mailout, if the current time is greater than the start time and less than the end time, all customers that match the filter values specified in this mailout must be selected from the database and sending should be started for all these customers.
- If a mailout is created with a start time in the future, the sending should start automatically on designated time without additional actions from the system user.
- In the course of sending messages, statistics should be collected for each message for subsequent reporting. See Message entity above.
- An external service that receives sent messages can process a request for a long time, respond with incorrect data, or not accept requests at all for some time. It is necessary to implement the correct handling of such errors. Problems with the external service should not affect the stability of the developed mailing service.
- If for some reason we did not have time to send all the messages, no messages should be delivered to customers after this time.

## Tech stack

<img src="https://img.shields.io/badge/FastAPI-fc884d?style=for-the-badge&logo=fastapi&logoColor=black"/> <img src="https://img.shields.io/badge/Pytest-fc884d?style=for-the-badge&logo=Pytest&logoColor=black"/> <img src="https://img.shields.io/badge/PostgreSQL-f5df66?style=for-the-badge&logo=PostgreSQL&logoColor=black"/> <img src="https://img.shields.io/badge/Docker-9a7b4d?style=for-the-badge&logo=Docker&logoColor=black"/>

## Tasks

- [x] API Dockerization.
- [x] Infrastructure with Docker Compose. Prepare docker-compose to start all project services with one command.
- [x] SQLModel for tables.
- [x] Connection with PostgreSQL.
- [x] Testing with Pytest. Write tests for the code.
- [x] Make it so that the page with Swagger UI opens at /docs/ and it displays a description of the developed API. Example: https://petstore.swagger.io.
- [x] Authentication using JWT.
- [x] Clear documentation on running the project with all its dependencies.
- [x] API documentation for integration with the developed service. Description of implemented methods in OpenAPI format.
- [ ] Obtaining general statistics on the created mailouts and the number of sent messages on them, grouped by status.
- [ ] Obtaining detailed statistics of sent messages for a specific mailout.
- [ ] Processing active mailouts and sending messages to customers.
- [ ] Provide automated build/testing with GitLab CI.
- [ ] Write configuration files (deployment, ingress, etc.) to run the project in Kubernetes and describe how to apply them to a running cluster.
- [ ] Implement an administrator Web UI to manage mailouts and get statistics on sent messages.
- [ ] Provide integration with an external OAuth2 authorization service for the administrative interface. Example: https://auth0.com.
- [ ] Implement an additional service that sends statistics on processed mailouts to an email address once a day.
- [ ] Implement the return of metrics in the prometheus format and document the endpoints and exported metrics.
- [ ] Provide detailed logging at all stages of request processing, so that during operation it is possible to find all information on:
  - mailout id: all logs for a specific mailout (both API requests and external requests to send specific messages);
  - message id: for a specific message (all requests and responses from an external service, all processing of a specific message);
  - customer id: any operations that are associated with a specific customer (adding, editing, sending a message, etc.).

## Database structure

![Schema](https://github.com/kooznitsa/test-projects/blob/main/mailing_service/api/db/db_schema.png)

## Endpoints

| Method             | Endpoint                                  | Description               |
|--------------------|-------------------------------------------|---------------------------|
| **---GENERAL**     | /                                         |                           |
| GET                | /                                         | Root                      |
| GET                | /docs                                     | Documentation             |
| GET                | /api                                      | Home                      |
| POST               | /auth/token                               | Login                     |
| POST               | /api/search                               | Search customer           |
| **---CUSTOMERS**   | **/api/customers/**                       |                           |
| POST               | /                                         | Add customers             |
| GET                | /                                         | Get customers             |
| GET                | /{customer_id}                            | Get customer by ID        |
| PUT                | /{customer_id}                            | Change customer by ID     |
| DELETE             | /{customer_id}                            | Delete customer by ID     |
| POST               | /{customer_id}/tags                       | Create customer tag       |
| POST               | /{customer_id}/tags/{tag_id}              | Delete customer tag       |
| **---MAILOUTS**    | **/api/mailouts/**                        |                           |
| POST               | /                                         | Add mailouts              |
| GET                | /                                         | Get mailouts              |
| GET                | /{mailout_id}                             | Get mailout by ID         |
| PUT                | /{mailout_id}                             | Change mailout by ID      |
| DELETE             | /{mailout_id}                             | Delete mailout by ID      |
| POST               | /{mailout_id}/tags                        | Create mailout tag        |
| POST               | /{mailout_id}/tags/{tag_id}               | Delete mailout tag        |
| POST               | /{mailout_id}/phone_codes                 | Create mailout phone_code |
| POST               | /{mailout_id}/phone_codes/{phone_code_id} | Delete mailout phone_code |
| **---MESSAGES**    | **/api/messages/**                        |                           |
| POST               | /                                         | Add message               |
| GET                | /                                         | Get mailouts              |
| GET                | /{message_id}                             | Get mailout by ID         |
| PUT                | /{message_id}                             | Change mailout by ID      |
| DELETE             | /{message_id}                             | Delete mailout by ID      |
| GET                | /stats                                    | Get messages stats        |
| **---PHONE CODES** | **/api/phone_codes/**                     |                           |
| POST               | /                                         | Add phone code            |
| GET                | /                                         | Get phone codes           |
| GET                | /{phone_code_id}                          | Get phone code by ID      |
| PUT                | /{phone_code_id}                          | Change phone code by ID   |
| DELETE             | /{phone_code_id}                          | Delete phone code by ID   |
| **---TIMEZONES**   | **/api/timezones/**                       |                           |
| POST               | /                                         | Add timezone              |
| GET                | /                                         | Get timezones             |
| GET                | /{timezone_id}                            | Get timezone by ID        |
| PUT                | /{timezone_id}                            | Change timezone by ID     |
| DELETE             | /{timezone_id}                            | Delete timezone by ID     |
| **---TAGS**        | **/api/tags/**                            |                           |
| PUT                | /{tag_id}                                 | Change tag by ID          |
| DELETE             | /{tag_id}                                 | Delete tag by ID          |

## Commands

- Create network so that Docker Compose can work: ```docker network create my-net```
- Start the containers: ```docker-compose up -d --build```
- Stop the containers: ```docker-compose down```
- Run tests: ```docker exec -it fastapi_service poetry run pytest```
- Run tests and get a coverage report: ```docker exec -it fastapi_service poetry run pytest --cov```