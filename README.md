# Understanding the MoMA's collection by race, gender and nationality.
This project uses the MoMA's public dataset to develop an understanding of the MoMA's artwork acquisitions by race, gender and nationality.

## Overview
This project is focused around the MoMA's public dataset of artworks and artists. Using this dataset, I will do time-series analysis on the MoMA's collecting patterns by race, gender and nationality. The analysis will give us a view on the MoMA's diversity when collecting artworks.

## Limitations of the Data
The MoMA's public dataset does not have information on the artist's race. To include information on race, I've combined the MoMA's artist dataset with the US census data of surnames, which can be used to deduce the probability of an surname's race. 

The MoMA's artist dataset has two limitations around gender. The first issue is that their definitions for gender are binary and so we are limited to either male or female. This does not work for artists who associate with neither male nor female, or for artist groups who have a composition of both male and female members. The second issue is that their gender dataset is largely incomplete for singular artists who do fit into the male/female gender binary - to resolve this issue, I've included an alternative dataset that looks at firstnames, from which we can deduce the probability of a firstname's gender.

## Data

### Primary dataset:

**The Museum of Modern Art (MoMA) Collection**
https://github.com/MuseumofModernArt/collection

### Complementary datasets:

**lastnames.json**:
API: https://api.census.gov/data/2010/surname.html

**summary (top1000) of lastnames**: 
https://www.census.gov/topics/population/genealogy/data/2000_surnames.html

**/names folder**
https://www.ssa.gov/oact/babynames/limits.html

## Authored Files

#### artist_exploration.ipynb
This notebook is used to explore the dataset data/artists.csv

#### artwork_exploration.ipynb 
This notebook is used to explore the dataset data/artworks.csv

#### data_prep.ipynb
This notebook reads in the datasets /data/names and /data/lastnames.json and transforms them such that they can be joined with the artist dataset provided by MoMA. The artist dataset is then merged with the artworks dataset in order to get race, gender and nationality data associated to each artwork collected by the MoMA. The outputof this notebook is a csv - ** /data/merged.csv **

#### analysis.ipynb
This notebook examines the MoMA's collection through the years by race, gender and nationality. Three time-series plots are shown in this notebook showing changes the MoMA's collection by these three aspects.
