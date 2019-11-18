# StudySpotter
## Team-GoodQuestion

[studyspotter.ca](https://studyspotter.herokuapp.com)

## Inspiration
We wanted to solve a real, everyday problem that affects us students!  Have you ever went to a library prepared to get stuff done, but end up wasting time looking for a good spot?  This problem has always plagued us. We decided to create StudySpotter to help people better use the study spaces available to them. 


## What it does
StudySpotter tracks a number of study locations across the world and provides a live feed to our website of how busy the location is.  The app is useful in avoiding spending unnecessary time, just wandering around libraries. It has really clean and eye-catching interfaces with a perfect color scheme and all interfaces are designed with beautiful color contrasts. 
Some study spaces are more full than others, but which one is more full? Good question! Our app can show and predict how busy the libraries are, and make recommendations based on real time and predicted population densities. So people can better use the spaces.

## How I built it
### The data pipeline
![The pipline](http://samuellando.com/pipeline.png)

In order to  capture a sense of how busy an area is. We decided to passively capture wireless network traffic in the form of wifi pings. These wifi pings are constantly transmitted by phones, laptops and other internet connected devices, and therefore can give us a relative sense of how busy a given location is through counting the number of unique MAC addresses.

This data is captured by distributed nodes(Raspberry Pis) at several physical locations and is transmitted to a centralized database using our open API. This API then allows the front-end of our site to query for information on how relatively busy a given building, floor and/or room is.

We then implemented a front-end for our API using Dash by Plotly. Our frontend allows users to view a map of several Montreal study locations and how busy/dense they are.

## Challenges I ran into
Our biggest challenge was learning Dash by Plotly. None of us had any experience using Dash or Plot.ly as a matter of fact.  It was a challenge but we sought help from the Plotly mentors which helped us tremendously.  

## Accomplishments that I'm proud of
We came up with a game plan that combined debate practice with team building. We were passionate about helping others by minimizing waste of time, so we decided to make our project more engaging and valuable. As a result, we were able to structure people's agenda more efficient.

## What I learned
The world has plenty of information but not enough inspiration. 
Working on this project, we experimented with a plotly.js site that used the GoogleMaps API but eventually settled on a Plotly Dash site that we hosted using Heroku.  We had to learn how to host with Heroku, as well as how to use Plotly Dash to create an information-rich, live website.

## What's next for FindSpotter
FindSpotter has a lot of potential for future growth. In the future, we would like to improve our site so that it recommends visitors locations to study which aren’t too busy.  Another thing we could do is implement our business tracking onto public buses.  People would be able to see roughly how many people are using the bus system and therefore decide if they want to take the bus for their morning commute or not.

