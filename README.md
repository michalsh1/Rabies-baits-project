# Rabies vaccine baits project
## This Django app was built for storing oral rabies vaccine drop data, manipulating it and calculating the scattering for desired dates.

<img src="https://github.com/michalsh1/rabies-baits-project/blob/master/Images/main%20picture.JPG" width="50%" height="50%">

<br>

## Background
Rabies is a viral disease which infects mammals, and can then be transferred by them to human beings. 
In order to control and stop the spread or rabies disease, Israel Nature and Parks Authority (INPA) & The Ministry of Agriculture and Rural Development are conducting an oral vaccination management program. In this program, baits containing rabies vaccines are being scattered throughout Israel. When predators consumes the baits, they are being vaccinated against the rabies virus, and that way the chain of infection breaks.

<br>

## Project's goal
In order to track the release of the baits, I was asked to create an app to store rabies vaccination data and to calculate the number of rabies baites that were released during a desired date, time and area.

<br>

## Assumptions and meta data of vaccine scattering:
1. Most of the baits are being released using airplanes.
2. Some of the baits are being scattered by foot by INPA rangers. 

<br>

## Original files

I was given different types of data, from different sources:

### 1. Airborne scattering routes files:

<br/>

- 540 GPX files of all the routes that were recorder by two different pilots.
    <br>


-   The file names were supposed to represent the date and the number of baits that were released and more info.


       ![GPX files](https://github.com/michalsh1/rabies-baits-project/blob/master/Images/gpx%20files.JPG "GPX files")


-   The files contained one or more routes (multi line strings) and points taken along the flight.


<br>


<img src="https://github.com/michalsh1/rabies-baits-project/blob/master/Images/gpx%20file%20example.JPG" width="70%" height="70%">
<br>
<br>


### 2. Route/point files for dispersal by foot

- These files were recorded using a different app, and might or might not include routes.

<br>
<br>

### 3. Scattering polygons 
- In cases where pilots didn't record the flight route- they gave a polygon where they scattered the baites.


<br>
<br>

### 4. Excel files
- these files are supposed to sum all the data that is related to the different routes and polygons.
- Each column consistes the following: date, number of baits released, area etc. 
![excel file](https://github.com/michalsh1/rabies-baits-project/blob/master/Images/excel%20example.JPG)


<br>

## Work process: airborne scatterring data
Most of the work was on cleaning airborne routes and generating a main data base with all data in the same format.

<br>

### First processing part: Cleaning airborne data using Django (Python)

Using Django, I uploaded the route from shp files into a Django model (SQLite).
<br>
I decided to disregard the points layers, as they were the same as the multi line string's points - and took into consideration only the rout layers.

<br>
I cleaned and transformed relevant data: file name, feature name, date and multi-line-string route. 
<br>
Those were saved in a temporary Django model in the data base.
<br>
Often, one shp file contained few MLS (Multi Line String) files - So I kept them all in the Django model.

<br>
In the end of this process I have had clean data model:each route with it's relevant meta data: date, original file and feature names.

<br>
<br>

### Second processing part: Cleaning data using QGIS and Excel

I exported the cleaned routes Django  model into shp files in order to check for duplications.
Then I cleaned the routes using QGIS:

1. I hava found all the double routes and kept only relevant files.
2. I removed all remainders from take-off, landing and of the flight to the scatterring area.
3. I mathced the route files to the excel file. That allowed:
    - To have number of bites for each route.
    - To find irragularities and issues to be solved later on.

<br>
<br>

### Third processing part: Uploading cleaned data into a SQLite data base using Django (class RoniRoutes)

I Generated a new model to store all routes in Django data base.
<br>
And I uploaded the clean airborne data into this model
<br>
<br>
<br>

## Work process: polygons of airborne data 


class RoniPolygons
As mentioned, in some cases I had only polygons of scatterring area. 
<br>

I decided to create a second model - of polygons. and Uploaded these polygons, after matching to excel file - in the new model (class RoniPolygons)




<br>
<br>
<br>

## Work process: scatterring by-foot

### routes:
I wrote a script to add this data to the cleaned route model (RoniRoutes).

<br>

### points:
In cases where I have had only points of scatterring - I created a polygon and added it to the Polygon model (RoniPolygons).
<br>

<br>
<br>
<br>

## Scatterring calculations:

I generated a new model that have pixels all along the area that I was asked to calculate scattering in.


Then, in order to calculate scattering - one should run the script ```roni_PixelByDate_calc.py```
<br>

This scripts checks the data in the two models- ```RoniRoutes``` and ```RoniPolygons```, to see if they are intersceting with the relevant pixel. And then updates a model called ```PixelByDate```. 
In each case where there has been an intersaction - a new pixel is generated with the date of scatterring, and the mean number of baites that were scattered in that pixel, based on the routes and polygons models.
 
Then, in order to answer the question "how many baits were scattered in X area in Y dates" : one can export the ```PixelByDate``` model data into json file using ```export_roni_data.py```, then load it to QGIS and interscet with desired polygon and filter by dates.


![PixelByDate_example]([https://github.com/michalsh1/rabies-baits-project/blob/master/Images/excel%20example.JPG](https://github.com/michalsh1/rabies-baits-project/blob/master/Images/PixelByDate_example.jpg))


<br>
<br>
<br>

## Notes:

- All data can be exported to json files - in order to make further calculations.
<br>
- This app could have a better UI, But for now- this results is enough for those who requested it.
