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


Assumptions and meta data of vaccine scattering:
1. Most of the baits are being released using airplanes.
2. Some of the baits are being scattered by foot by INPA rangers. 

<br>
<br>

## Original files

I was given different types of data, from different sources:

1. Airborne scattering routes files:
- 540 GPX files of all the routes that were recorder by two different pilots.

    -   The file names were supposed to represent the date and the number of baits that were released and more info.


    ![GPX files](https://github.com/michalsh1/rabies-baits-project/blob/master/Images/gpx%20files.JPG "GPX files")


    -   The files contained one or more routes (multi line strings) and one or more points taken along the flight. I decided to disregard the points layers, as they were the same as the milti line string's points - and took into consideration only the rout layers.




<br>

<p align="center">

<img src="https://github.com/michalsh1/rabies-baits-project/blob/master/Images/gpx%20file%20example.JPG" width="70%" height="70%">
</p>
<br>
<br>

2. Route files for dispersal by foot

- These files were recorded using a different app, and might or might not include routes.

<br>
<br>

3. Scattering polygons 
- In cases where pilots didn't record the flight route- they gave a polygon where they scattered the baites.


<br>
<br>

4. Excel files
- these files are supposed to sum all the data that is related to the different routes and polygons.
- Each column consistes the following: date, number of baits released, area...
![excel file](https://github.com/michalsh1/rabies-baits-project/blob/master/Images/excel%20example.JPG)


<br>

## Work process

### First processing part: Cleaning data using Django

First I cleaned all data from different sources, and load it into main data base.

<br>

Using Django (Python) I uploaded the route from shp files into a Django model (SQLite).
I cleaned and transformed relevant data: file name, feature name, date and multi-line-string route. Those were saved in the route model in the data base.
Often, one shp file contained few MLS (Multi Line String) files - So I kept them all in the Django model.

<br>
In the end of this proess I had clean data model: I had each route with it's relevant meta data: date, original file and feature names.



### Second processing part: Cleaning data using QGIS and Excel

I exported the cleaned routes Django  model into shp files in order to check for duplications.
Then I cleaned the routes using QGIS:

1. I hava found all the double routes and kept only relevant files.
2. I removed all remainders from take-off, landing and of the flight to the scatterring area.
3. I mathced SHP files to the excel file. That allowed:
- To have number of bites for each route.
- To find irragularities and issues to be solved later on.



### Third processing part: Uploading cleaned data into a unified SQLite data base using Django

I Generated a new model to store all routes in Django data base.

<br>

<br><br><br><br>



#WORK IN PROGRESS
