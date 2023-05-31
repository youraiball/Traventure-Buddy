document.querySelector("#find-act").addEventListener("click", (evt) => {
    evt.preventDefault();

    const city = document.querySelector("#city").value;
    const country = document.querySelector("#country").value;
    const fromDate = document.querySelector("#from").value;
    const toDate = document.querySelector("#to").value;
    const queryString = new URLSearchParams({ 
        city: city,
        country: country,
        from: fromDate,
        to: toDate
    }).toString();
    if (city !== '' && country !== '') {
        fetch (`/api/activities?${queryString}`)
            .then(response => response.json())
            .then((activityData) => {
                document.querySelector("#all-activs").style.display = "";
                document.querySelector("#place-title").innerHTML = `${activityData.city}, ${activityData.country}`;

                if (activityData.fromDate !== "" && activityData.toDate !== "") {
                    document.querySelector("#date-title").innerHTML = `${activityData.fromDate} - ${activityData.toDate}`;
                }
                
                document.querySelector("#loader").classList.add("d-none");

                if (activityData.activities.length !== 0) {
                    for (const activity of activityData.activities){
                        document.querySelector("#activities-list").insertAdjacentHTML("beforeend", `<li>
                        <a href="/activities/${activity.activityId}">
                            ${activity.name}
                        </a></li>`);
                    }
                    document.querySelector('#save-btn').style.display = "";
                    document.querySelector('#save-btn').addEventListener("click", () =>{
                        const data = {
                            destId: activityData.destId,
                            city: activityData.city,
                            country: activityData.country
                        };

                        fetch("/api/save-list", {
                            method: "POST",
                            body: JSON.stringify(data),
                            headers: {
                                "Content-Type": "application/json"
                            }
                        })
                            .then((response) => response.json())
                            .then((responseJson) => {
                                document.querySelector("#status-ctn").innerHTML = responseJson.status
                                if (responseJson.status === true) {
                                    document.querySelector("#status-ctn").classList.add("alert", "alert-success");
                                } else {
                                    document.querySelector("#status-ctn").classList.add("alert", "alert-danger");
                                    window.scrollTo(0,0);
                                };
                            });
                    });
                } else {
                    if (activityData.user !== "") {
                        document.querySelector("#sorry-msg").innerHTML = `Sorry, ${activityData.user}.`;
                    } else {
                        document.querySelector("#sorry-msg").innerHTML = "Sorry, Traveler.";
                    }
                    document.querySelector("#no-activities").style.display = "";
                }
            });
        document.querySelector("#search").style.display = "none";
        document.querySelector("#loader").classList.remove("d-none");
    } else {
        document.querySelector("#status-ctn").innerHTML = "Please enter a valid destination.";
        document.querySelector("#status-ctn").classList.add("alert", "alert-danger");
    }
});
