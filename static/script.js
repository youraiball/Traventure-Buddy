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

    fetch (`/api/activities?${queryString}`)
        .then(response => response.json())
        .then((activityData) => {
            document.querySelector("#all-activs").style.display = "";
            document.querySelector("#place-title").innerHTML = `${activityData.city}, ${activityData.country}`;
            
            if (activityData.fromDate !== "" && activityData.toDate !== "") {
                document.querySelector("#date-title").innerHTML = `${activityData.fromDate} - ${activityData.toDate}`;
            }
            
            document.querySelector("#loader").style.display = "none";

            if (activityData.activities.length !== 0) {
                for (const activity of activityData.activities){
                    document.querySelector("#activities-list").insertAdjacentHTML("beforeend", `<li>
                    <a href="/activities/${activity.activity_id}">
                        ${activity.name}
                    </a></li>`);
                }
            } else {
                document.querySelector("#activities-ctn").insertAdjacentHTML("beforend", `<h3>
                Sorry, 
                {% if "user" in session %} 
                    {{ user.fname }}.
                {% else %}
                    Traveler.
                {% endif %}  Looks like Traventure Buddy hasn't quite explored this destination yet.
            </h3>
            <h5>There are no activities available at the moment but you can be the trail blazer!</h5>`);
            }
        });
    document.querySelector("#search").style.display = "none";
    document.querySelector("#loader").style.display = "";
});


// const loader = () => {
//     setTimeout(showPage, 3000);
// }

// function showPage() {
//   document.getElementById("loader").style.display = "none";
//   document.getElementById("all-activs").style.display = "block";
// }