# Aviasales Webservice

## Task Description
Two XML files are available ([file 1](https://github.com/KosyanMedia/test-tasks/blob/master/assisted_team/RS_ViaOW.xml), [file 2](https://github.com/KosyanMedia/test-tasks/blob/master/assisted_team/RS_Via-3.xml)).

These are results of search queries made to one of Aviasales partners. The results contain flight options (the Flights tag) with all the necessary information to display the ticket on Aviasales.

Based on this data, you need to make a web service with endpoints that give answers to the following questions:

- What flight options from DXB to BKK do we get?
- What are the most expensive / cheapest, fastest/longest routes, and best options?
- What are the differences between the results of the two queries (changing routes/conditions)?

Implementation language: Python 3, format: JSON + libraries and tools of your choice.

We will evaluate the ability to perform a task with incomplete data about it, the ability to make decisions independently, and the quality of the code.

## Tech Stack
<img src="https://img.shields.io/badge/Python-d93b32?style=for-the-badge&logo=python&logoColor=black"/> <img src="https://img.shields.io/badge/Django-fc884d?style=for-the-badge&logo=django&logoColor=black"/> <img src="https://img.shields.io/badge/PostgreSQL-f5df66?style=for-the-badge&logo=PostgreSQL&logoColor=black"/>

## Database Structure
![database-diagram.png](https://raw.githubusercontent.com/kooznitsa/test-projects/main/aviasales-webservice/database/database_diagram.png)

## Project Structure

### Main page: all flights
Sorting options:
- by price ASC
- by price DESC
- by flight time ASC
- by flight time DESC
![all_flights.png](https://raw.githubusercontent.com/kooznitsa/test-projects/main/aviasales-webservice/screenshots/all_flights.png)

### Best options
Criteria:
- Direct flights or
- Cheap flights or
- Fast flights
![best_options.png](https://raw.githubusercontent.com/kooznitsa/test-projects/main/aviasales-webservice/screenshots/best_options.png)

### Requests comparison
![flight_stats.png](https://raw.githubusercontent.com/kooznitsa/test-projects/main/aviasales-webservice/screenshots/flight_stats.png)

### API
- Top 10 cheapest flights
- Top 10 most expensive flights
- Top 10 falstest flights
- Top 10 longest flights
![api_fastest.png](https://raw.githubusercontent.com/kooznitsa/test-projects/main/aviasales-webservice/screenshots/api_fastest.png)

### API (web)
![top_cheapest.png](https://raw.githubusercontent.com/kooznitsa/test-projects/main/aviasales-webservice/screenshots/top_cheapest.png)