# Baits project
![img](https://github.com/michalsh1/rabies-baits-project/blob/master/Images/main%20picture.JPG)

<br>

## Background:
Rabies is a viral disease which infects mammals, and can then be transferred by them to human beings. 
In order to control and stop the spread or rabies disease, Israel Nature and Parks Authority (INPA) & The Ministry of Agriculture and Rural Development are conducting an oral vaccination management program. In this program, baits containing rabies vaccines are being scattered throughout Israel. When predators consumes the baits, they are being vaccinated against the rabies virus, and that way the chain of infection breaks.

<br>

## Project's goal:
In order to track the release of the baits, We wanted to know how many rabies baites were being released during a specific date, time and area.

<br>
<br>

Methods of scattering the baits:
1. Most of the baits are being released using airplanes.
2. Some of the baits are being scattered by foot by INPA rangers. 

<br>
<br>

## Original files:
At the beginning I was given the following files:
- 540 GPX files of all the routes that were recorder by two different pilots.

    -   The file names were supposed to represent the date and the number of baits that were released and more info.
    -   The files contained one or more routes (multi line strings) and one or more points taken along the flight. I decided to disregard the points layers, and take into consideration only the routs layers.

<center>


![GPX files](https://github.com/michalsh1/rabies-baits-project/blob/master/Images/gpx%20files.JPG)

<br>

<br>

<!--
![GPX file example](https://github.com/michalsh1/rabies-baits-project/blob/master/Images/gpx%20file%20example.JPG) 
 -->

<img src="https://github.com/michalsh1/rabies-baits-project/blob/master/Images/gpx%20file%20example.JPG" width="70%" height="70%">
</center>

<br>

- Excel files with the management calculations for each year. Each column consisted the following: date, number of baits released, area...
![excel file](https://github.com/michalsh1/rabies-baits-project/blob/master/Images/excel%20example.JPG)


<br>

## Work process

### Cleaning SHP files
using QGIS I had to find all doubles and keep only relevant file

I mathced SHP files to the excel in order to find irragularities and issues to be solved.

<br>

### Creating a database using Django (SQLite)

<br><br><br><br>
