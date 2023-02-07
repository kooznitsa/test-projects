let flightsUrl = "http://127.0.0.1:8000/api/cheapest-flights";

let getFlights = () => {
    fetch(flightsUrl, {
            method: "GET",
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            buildFlights(data);
        })
}

let buildFlights = (flights) => {
    let flightsWrapper = document.getElementById("flights-wrapper");
    flightsWrapper.innerHTML = "";

    for (let i in flights) {
        let flight = flights[i];

        let flightCard = `
                <div class="card mb-5">
                    <div class="card-header">
                        <h4 class="card-title">ROUTE ${flight.container_count}</h4>
                    </div>
                    <div class="card-body">
                        <p>REQUEST TIME: ${flight.request_time}</p>
                        <p>PRICE: <strong class="text-primary">${flight.currency.currency} ${flight.adult_price}</strong></p>
                        <p>PRICE TYPE: ${flight.itineraries[0].priced_itinerary.priced_itinerary}</p>
                        <p>TOTAL FLIGHT TIME: ${flight.itineraries[0].total_flight_time} min</p>
                    </div>   
        `;

        for (let i in flight.itineraries[0].flights) {
            let f = flight.itineraries[0].flights[i];

            flightCard += `
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item">
                            <p><strong>FLIGHT PART ${f.flight_part} — FROM ${f.source.city} TO ${f.destination.city}</strong></p>
                            <p>FLIGHT NO.: ${f.flight_num} ${f.carrier.carrier} (Class ${f.class_field.class_field})</p>
                            <p>ARRIVAL TIME: ${f.arrival_time}</p>
                            <p>DEPARTURE TIME: ${f.departure_time}</p>
                            <p>FLIGHT TIME: ${f.flight_time} min</p>
                        </li>
                    </ul>
            `;
        }

        flightCard += `
                </div>
            `;

        flightsWrapper.innerHTML += flightCard;
    }
}


getFlights();