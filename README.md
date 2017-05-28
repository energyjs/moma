# moma
Understanding the MoMA's artwork acquisitions by race, gender and nationality.

## Overview
This project is focused around the MoMA's public dataset of artworks and artists. Using this dataset, I will do time-series analysis on the MoMA's collecting patterns by race, gender and nationality. The analysis will give us a view on the MoMA's diversity when collecting artworks.

## Limitations of the Data
The MoMA's public dataset does not have information on the artist's race. To include information on race, I've combined the MoMA's artist dataset with the US census data of surnames, which can be used to deduce the probability of an surname's race. 

The MoMA's artist dataset has two limitations around gender. The first issue is that their definitions for gender are binary and so we are limited to either male or female. This does not work for artists who associate with neither male nor female, or for artist groups who have a composition of both male and female members. The second issue is that their gender dataset is largely incomplete for singular artists who do fit into the male/female gender binary - to resolve this issue, I've included an alternative dataset that looks at firstnames, from which we can deduce the probability of a firstname's gender.

## Complementary datasets:

**lastnames.json**:
API: https://api.census.gov/data/2010/surname.html

**summary (top1000) of lastnames**: 
https://www.census.gov/topics/population/genealogy/data/2000_surnames.html

**/names folder**
https://www.ssa.gov/oact/babynames/limits.html
