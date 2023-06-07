document.querySelector("#find-act").addEventListener("click", (evt) => {
    evt.preventDefault();

    const city = document.querySelector("#city").value;
    const country = document.querySelector("#country").value;
    const queryString = new URLSearchParams({ 
        city: city,
        country: country,
    }).toString();
    if (city !== '' && country !== '') {
        fetch (`/api/activities?${queryString}`)
            .then(response => response.json())
            .then((activityData) => {
                document.querySelector("#all-activs").style.display = "";
                document.querySelector("#place-title").innerHTML = `${activityData.city}, ${activityData.country}`;
                
                document.querySelector("#loader-ctn").classList.add("d-none");

                if (activityData.activities.length !== 0) {
                    for (const activity of activityData.activities){
                        document.querySelector("#activities-list").insertAdjacentHTML("beforeend", `
                        <a class="list-group-item list-group-item-action" href="https://www.google.com/search?q=${activity.name} ${activityData.country}" target="_blank" data-bs-toggle="tooltip" data-bs-placement="bottom" data-bs-title="Activity Type: ${activity.type}">
                            ${activity.name}
                        </a>`);
                    }
                    // Initialize tooltips to use
                    const tooltipTriggerList = document.querySelectorAll("[data-bs-toggle='tooltip']");
                    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

                    document.querySelector("#destination-img").src = activityData.destImg;
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
                                if (responseJson.success === true) {
                                    document.querySelector("#status-ctn").classList.add("alert", "alert-success");
                                } else {
                                    document.querySelector("#status-ctn").classList.add("alert", "alert-danger");
                                }
                                window.scrollTo(0,0);
                            });
                    });
                } else {
                    document.querySelector("#activities-list").classList.add("d-none");
                    if (activityData.user !== "") {
                        document.querySelector("#sorry-msg").innerHTML = `Sorry, ${activityData.user}.`;
                    } else {
                        document.querySelector("#sorry-msg").innerHTML = "Sorry, Traveler.";
                    }
                    document.querySelector("#no-activities").style.display = "";
                }
            });
        document.querySelector("#search").style.display = "none";
        document.querySelector("#loader-ctn").classList.remove("d-none");
    } else {
        document.querySelector("#status-ctn").innerHTML = "Please enter a valid destination.";
        document.querySelector("#status-ctn").classList.add("alert", "alert-danger");
    }
});
