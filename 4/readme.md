# Objective

### Writing your own MapReduce Function

## Overview

Write a MapReduce application to find the mean maximum recorded temperature for every day of the year for every weather station, from the NCDC data records from 1901-1905. You can access the data in our Hadoop cluster /user/chatree/ncdc_data/ or download them from here: ncdc_data.tar.gz.

To calculate the mean maximum temperature for station 029070-99999 on Jan 1, first, you need to calculate the maximum temperature for this station on January 1, 1901; January 1, 1902; ...; January 1,1905. Then calculate the mean from these values.

Note: The station identifier can be extracted from character char[4-14], date: char[15-22]  ( month:char[19-20] and day: char[21-22]), temperature: char[87-91], and quality char[92].

To get you to start, you can take a look at the simple MapReduce job that finds the maximum temperature for each year below:

        Java
            MaxTemperature.javaClick for more options
            MaxTemperatureMapper.java
            MaxTemperatureReducer.javaClick for more options
        Python
            max_temperature_map.pyClick for more options
            max_temperature_reduce.py
Note: how to chain multiple MapReduce jobs 

### What to Submit

The screen output when running the job

The output file(s) as the result of running the job

