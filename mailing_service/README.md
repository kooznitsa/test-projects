# Mailing service

[Original task in Russian](https://www.craft.do/s/n6OVYFVUpq0o6L)

## Task description

- Implement methods for creating a new mailout, viewing the created ones, and getting statistics on completed mailouts.
- Implement the service itself for sending notifications to an external API.

## Criteria

- The completed task must be placed in a public repository on gitlab.com.
- Clear documentation on running the project with all its dependencies.
- API documentation for integration with the developed service.
- Description of implemented methods in OpenAPI format.

## Main task

Design and develop a service that launches a mailout according to a mailing list of customers.

### Attributes of entities

- Mailout:
  - Unique id
  - Date and time of mailout start
  - Text message for a customer
  - Customer filter (phone code, tag)
  - Date and time of mailout finish
  - Time interval in which you can send messages to clients, taking into account their local time. Do not send a message to the customer if their local time is not within the specified interval

- Customer:
  - Unique id
  - Phone number (7XXXXXXXXXX)
  - Mobile operator code
  - Tag
  - Time zone

- Message:
  - Unique id
  - Date and time of creating/sending the message
  - Sending status
  - Mailout id
  - Customer id

### API functionality

- Customer:
  - Adding a new customer to the database with all its attributes
  - Updating customer attribute data
  - Deleting a customer from the database

- Mailout:
  - Adding a new mailout with all its attributes
  - Obtaining general statistics on the created mailouts and the number of sent messages on them, grouped by status
  - Obtaining detailed statistics of sent messages for a specific mailout
  - Updating mailout attributes
  - Deleting mailout
  - Processing active mailouts and sending messages to customers

### Mailout logic

- After creating a new mailout, if the current time is greater than the start time and less than the end time, all customers that match the filter values specified in this mailout must be selected from the database and sending should be started for all these customers.

- If a mailout is created with a start time in the future, the sending should start automatically on designated time without additional actions from the system user.

- In the course of sending messages, statistics should be collected for each message for subsequent reporting. See Message entity above.

- An external service that receives sent messages can process a request for a long time, respond with incorrect data, or not accept requests at all for some time. It is necessary to implement the correct handling of such errors. Problems with the external service should not affect the stability of the developed mailing service.

- If for some reason we did not have time to send all the messages, no messages should be delivered to customers after this time.

### External Send Service API

To integrate with the project under development in this task, there is an external service that can receive requests to send messages to customers.

The OpenAPI specification is located at: https://probe.fbrq.cloud/docs

This API assumes authentication using JWT.

## Additional tasks that increase the candidate's chances

- Write tests for the written code
- Provide automated build/testing with GitLab CI
- Prepare docker-compose to start all project services with one command
- Write configuration files (deployment, ingress, etc.) to run the project in kubernetes and describe how to apply them to a running cluster
- Make it so that the page with Swagger UI opens at /docs/ and it displays a description of the developed API. Example: https://petstore.swagger.io
- Implement an administrator Web UI to manage mailouts and get statistics on sent messages
- Provide integration with an external OAuth2 authorization service for the administrative interface. Example: https://auth0.com
- Implement an additional service that sends statistics on processed mailouts to an email address once a day
- Implement the return of metrics in the prometheus format and document the endpoints and exported metrics
- Provide detailed logging at all stages of request processing, so that during operation it is possible to find all information on
  - mailout id: all logs for a specific mailout (both API requests and external requests to send specific messages)
  - message id: for a specific message (all requests and responses from an external service, all processing of a specific message)
  - customer id: any operations that are associated with a specific customer (adding, editing, sending a message, etc.)


## Implementation

### Tech stack

- API Dockerization.
- Infrastructure with Docker Compose.
- SQLModel for tables.
- Connection with PostgreSQL.
- Testing with Pytest.

### Database structure

![Schema](https://github.com/kooznitsa/test-projects/blob/main/mailing_service/api/db/db_schema.png)

### Endpoints

| Method        | Endpoint                               | Description              |
|---------------|----------------------------------------|--------------------------|
| GENERAL       |                                        |                          |
| GET           | /                                      | Home                     |
| POST          | /search                                | Search                   |
| POST          | /auth/token                            | Login                    |
| CUSTOMERS API |                                        |                          |
| GET           | /api/customers/                        | Get customers            |
| POST          | /api/customers/                        | Add customers            |
| GET           | /api/customers/{id}                    | Get customer by ID       |
| PUT           | /api/customers/{id}                    | Change customer by ID    |
| DELETE        | /api/customers/{id}                    | Delete customer by ID    |
| MAILOUT API   |                                        |                          |
| GET           | /api/mailouts/                         | Get mailouts             |
| POST          | /api/mailouts/                         | Add mailouts             |
| GET           | /api/mailouts/{id}                     | Get mailout by ID        |
| PUT           | /api/mailouts/{id}                     | Change mailout by ID     |
| DELETE        | /api/mailouts/{id}                     | Delete mailout by ID     |
| GET           | /api/mailouts/status/stats             | Get mailout stats        |
| MESSAGES API  |                                        |                          |
| POST          | /api/mailouts/{id}/messages            | Add message              |
| GET           | /api/mailouts/{id}/messages/stats      | Get messages stats       |

### Commands

Create our Network so that Docker Compose can work:
```
docker network create my-net
```

Start the containers:
```
docker-compose up -d --build
```

Stop the containers:
```docker-compose down```

See relations in the database mailing_db:
```
docker exec -it db_postgres psql -U postgres
\dn                                           # list namespaces
set search_path to pg_database_owner,public;
\c mailing_db
\dt
```

Run tests:
```
docker exec -it fastapi_service poetry run pytest
```