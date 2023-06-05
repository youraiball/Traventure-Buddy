fetch("/api/get-tripcount")
    .then((response) => response.text())
    .then((totalTrips) => {
        document.querySelector("#tripcount").innerHTML = totalTrips;
    });