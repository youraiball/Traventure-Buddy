# Traventures - Hackbright Academy Capstone Project

## Overview
Traventures is a web app that helps travelers search for things to do at a particular destination. Users can enter a destination in the form of a city and country, and will be presented with a list of activities, along with a photo of that destination. Hovering their mouse over an activity will show whether that activity is a restaurant, shopping, or a tourism activity. If users click on an activity, a new tab will open with a google search of that activity. There is an option to save the search results for later viewing if users create an account and log in, and also the option to delete the list from a user's profile.

## Tech Stack
Python, PostgreSQL, SQLAlchemy, HTML, CSS, Bootstrap, JavaScript, AJAX, Flask, Jinja, Python Country-Converter

## API's
OpenTripMap - used to generate longitude & latitude coordinates to use in Geoapify API call
Geoapify - generate activities by categories
Google Custom Search Engine - get a stock image of a destination

## Features
### Activities Search by Destination
On Traventures' landing page, travelers will be able to search for recreational activities to do at a desired destination. To do so, they must provide a city and country. Upon clicking the "Find Activities" button, Traventures will begin by using the city and country to retrieve the appropriate longitude and latitude coordinates. To accomplish this, the country is converted into its respective ISO2 country code, which is then utilized along with the city as API parameters when calling the OpenTripMap API. Once the coordinates are retrieved, a SQL Alchemy query is executed to locate the destination in the database, if it exists. If it does, Traventures will execute another SQL Alchemy query to retrieve a list of activities related to tourism, restaurants, and shopping for that existing destination from the database. If the destination currently does not exist in the database, it will be saved to the database and Traventures will call the Geoapify API to retrieve a curated list of activities and save these to the database as well. This will allow for faster searches for the inputted destination in the future.

Geoapify stores places/businesses sorted by categories, for example hotels would fall under the category of accomodations, and restaurants would fall under catering. So the api wasn't just called once for all activites everytime there was a search. Rather, there were 4 separate api calls made for each destination, one for different categories as the parameter. So restaurant activities were retrieved by calling the api with "catering" as one of the parameters, shopping activities were called with the parameter "commercial," and two calls were made for tourism activities. One call with "tourism" as the parameter and the other call, "entertainment."

### Trips
Traventures users will have the ability to save each destination with its list of activities as a trip that is viewable from their profile page. Each trip on the user profile page will be a separate card titled as the destination with an appropriate destination image. Clicking on a trip will allow the user to view the same list of activities that they originally saw when searching that destination. Users may also delete trips by clicking on a trip from their user profile and hitting the "Delete" button.

### Retrieving Destination Images
To add high-quality destination images, Traventures utilizes the Google Custom Search Engine (CSE) API to locate Google Images matched against the destination city and country. Originally, destination images were retrieved using the Google Places API, but only results of user-uploaded images were being returned. Sometimes these images were of random buildings or objects within the destination, so they were not reliable or sufficient enough to show off as a destination image. Therefore, Google CSE was used to best handle this problem.

### Open Google search results for each activity
A shortcoming of the Geoapify API is that it only returns names of activities along with its categorized types pertaining to a location. This made creating an individual details page per activity difficult as there was no information to provide Traventures users any value. As a result, a design decision was made to automatically open a Google search results page of each activity per destination in a new tab to best guide the user towards finding any information or details they may need.

## Planned Roadmap
- let users add their own activities to a destination
- users can also delete activities they added
- clicking on one of the carousel images on the landing page, would take users to activities at that destination, rather than entering a city & country and clicking the "Find Activities" button
 