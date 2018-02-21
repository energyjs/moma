# An Analysis of the MoMA's Collection by Race and Gender
This project uses the MoMA's public dataset to develop an understanding of the MoMA's artwork acquisitions by race and gender.

To jump straight into the analysis, checkout the notebook: [/code/analysis.ipynb](/code/analysis.ipynb)

## Overview
In this project, we will try to understand the MoMA's collection from the standpoint of demographic and geographic diversity, and identify any trends in the MoMA's collecting tendencies with regards to race and gender.

## Data

In this project, the primary data set is data that is published by the Museum of Modern Art themselves. Because their data is relatively small, I copied `Artworks.csv` from their repo into `/data`. The MoMA consistently updates their dataset - this analysis was done on their Artworks data collected on 2/15/2018. 

**The Museum of Modern Art (MoMA) Collection**

URL: https://github.com/MuseumofModernArt/collection/blob/master/Artworks.csv

**lastnames.json**

API: https://api.census.gov/data/2010/surname.html

**Race distribution in the US** (this dataset is hardcoded directly into the notebook `/code/analysis.ipynb`)

URL: https://www.kff.org/other/state-indicator/distribution-by-raceethnicity 

### Limitations of the Data
This datasets primary limitation is that it uses a binary definition of gender and so we are limited to either male or female. This does not work for artists who do not conform to the male/female gender binary, and for artist groups that have multiple members of which there could be multiple genders.

Additionally, there are a lot of NaN values in the dataset for nationality and gender. About 12% of the dataset has values of NaN for gender.

## Directory Structure

This project is structured such that the following folders are located at root:
- /code
  - analysis.ipynb _[primary notebook containing analysis]_
  - util.py _[contains helper functions used in analysis.ipynb]_
- /data
  - lastnames.json _[mapping of lastname to likelihood of race]_
  - artworks.csv _[primary dataset containing the MoMA's collected artwork data]_

## Requirements
In order to run the notebook, you do not need to download any data as all the data needed is contained directly in the repo. You will need the following dependencies:
- python (>=3.4)
- matplotlib (>=2.1.0)
- pandas (>=0.20.3)
- numpy (>=1.13.3)
- jupyter notebook
