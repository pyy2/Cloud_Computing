# Objective

### Learn how to use basic Apache Spark to cache and process data in memory
### Learn how to submit a scala application to Spark


## Overview

Use Spark to calculate a variance of a collection of 100 numbers, randomly generated in range 1-100.  It must calculate in one-pass, ie. without computing the means first. See lecture note. You can use the code below as the starting point

=================================

    class RunningVar {
    // declare var here
    var ...

    // Compute initial variance for numbers 
    def this(numbers: Iterator[Double]) { 
    numbers.foreach(this.add(_))
    } 

    // Update variance for a single value 

    def add(value: Double) {
    ... 
    } 

    // Merge another RunningVar object and update variance 
    def merge(other: RunningVar) = { 
    ... 
    } 
    } 

    // generate 100 random numbers, valued randomly generated from 1 to 100

    val random_numbers = (1 to 100).map(x => Random.nextInt(100))

    // now setup to parallelize the computation ...

    val intRDD = ...

    var result = intRDD .mapPartitions(v => Iterator(new RunningVar(v))) .reduce((a, b) => a.merge(b))

    assert(result === intRDD.variance())

====================================

### What to Submit

Your code

The console output after you run it
