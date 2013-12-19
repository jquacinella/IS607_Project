Description of Final Project
============================

Prepared by: James Quacinella

## Summary 

### Description of "Food Stamps", or SNAP

The Supplemental Nutrition Assistance Program, also known as "The Food Stamp Program", is a federal aid program which provides financial assistance for purchasing food to low- and no-income people living in the U.S.  This program is administered by the U.S. Department of Agriculture, though benefits are distributed by individual U.S. states. They can be used to purchase any prepackaged edible foods, regardless of nutritional value (e.g. soft drinks and confections). 

The "Food and Nutrition Service" relies on data from the SNAP Quality Control (SNAP QC) database, to monitor changes in population and policy over time. This database is an "edited version of the raw datafile of monthly case reviews conducted by State SNAP agencies to assess the accuracy of eligibility determinations and benefit calculations for each State’s SNAP caseload". Documentation from the Dept of Agriculture describes the process each state goes through to provide, from making sure populations are not oversampled, and how many samples to submit based on state population. This document also describes how the Federal government cleans the raw State data to create the SNAP QC database ^[1][1] .


### Hypothesis

I'll be invetsigating if there is a trend over time for SNAP receipients to pay more rent as a percentgae of their income. This trend can be broken down over many demographies, like where someone lives, their race or age. My suspicion is that those receiving SNAP benefits pay more of their income go to rent as time goes on, especially in bigger cities. The data from any given year has samples of data that are reported to the federal government by the individual states. The data set provides two columns, one for reported rent and reported total income, which can be used to calculate the percentage of income going to rent for any sample. I'm hoping that this can be graphed over time.


### 'Business' Value

Having a deep understanding of the citizens who are using Food Stamps, including their behaviour and how they react to outside changes in the economy and government policy, is critical to smart governance. This deep understanding should be guided and informed by data. The specific hypothesis, that the beneficiaries of government help are seeing more of their income go towards a rising rent burden, is just one of many that city, state of the federal government should be concerned about. In this specific data set, each 'SNAP unit' has approximately 760 variables (depending on the year of collection), allowing for many different views on this one data set.

## TODO:

* Make sure graphs are labeled well
* Find original website of data, link to it
* Create decision tree trying to predict calculated column (?)
* Create map of USA showing scale of average % of income spent on rent
* Show some state-level data

## Methodology

### Summary

1. Load the data from 2011, the latest data that has been released. Explore the data, find any oddities or interesting points
2. Load all years of the data set, which ranges from 2002 - 2011, into multiple data frames
3. Calculate a new column, which is the "rent" column divided by "net income" column, for each data frame.
4. Look at the distribution (histogram, density plot) of the % income rent for all data sets
  * Is there a general increase? Show a boxplot per year, and see how the distribution of values changes over time
6. Generate map-based plot of this calculated value 

### Preparing the Data

The data from the government website had many different formats, none of which seemed to do well for R^[2][2] . I looked for ways of dealing with SAS and Stata file formats. I came across PyDTA, a python module that can read in DTA (Stata) files^[3][3] . I originally wrote a script ([exporter.py](https://github.com/jquacinella/IS607_Project/blob/master/exporter.py)) to convert the DTA file into a CSV file. However, this turned out to not be needed, as another website hosted by Penn State has copies of the data in CSV^[4][4] .

After dowloading all the years, we need to load the data into a list of data frames (one per year).


### Load Data

This snippet of code is responsible for loading the _snap_data_frames_ list. One function is used for loading a data frame from a given year, while another function calls this repeatedly for years 2002 - 2011. Note, after we load the data in the _snap_data_frames_ variable, we save it to disk to speed up the execution in the future.


```r
# Set the correct path
setwd("~/Code/Masters/IS607/Project/")

# Save original PAR value
op <- par(no.readonly = TRUE)

# Global values of year range
YEAR_MAX <- 2011
YEAR_MIN <- 2002

# Function will load and return one year of the SNAP data
load_snap_data <- function(year) {
    read.csv(paste("snap/snap_", as.character(year), ".csv", sep = ""))
}

# Function will load and return SNAP data for given date range (defaults to
# all years)
load_all_snap_data <- function(year_from = YEAR_MIN, year_to = YEAR_MAX) {
    snap_data_frames <- list()
    
    for (year in seq(year_from, year_to)) {
        data <- load_snap_data(year)
        snap_data_frames[[year]] <- data
    }
    
    return(snap_data_frames)
}

# Call the function to load all the data if its not on disk
if (!file.exists("snap_data_frames")) {
    snap_data_frames <- load_all_snap_data()
    save(list = "snap_data_frames", file = "snap_data_frames")
} else {
    load("snap_data_frames")
}
```


### Cleaning the Data

The data was generally very clean, and didn't require anything to do done to it. However, SNAP data from previous years was difficult to get, due to the bad web interface from Penn. I mistakenly downloaded truncated files and did not see that there were missing rows from many data sets.

### Plot Histogram of Wages

The column _FSGRINC_ (which is the sum of _FSEARN_ and _FSUNEARN_) is the Final Gross Countable Unit Income. We'll use this as a measure of how much money the SNAP unit is making. The first set of graphs show a histogram of _FSGRINC_ from 2011 versus 2002.


```r
par(mfrow = c(1, 2))
hist(snap_data_frames[[2011]]$FSGRINC, ylab = "Frequency", xlab = "Gross Income", 
    main = "Histogram of FSGRINC (2011)", breaks = 50, xlim = c(0, 5000))
hist(snap_data_frames[[2002]]$FSGRINC, ylab = "Frequency", xlab = "Gross Income", 
    main = "Histogram of FSGRINC (2002)", breaks = 50, xlim = c(0, 5000))
```

![plot of chunk unnamed-chunk-2](figure/unnamed-chunk-2.png) 


Lets compare the density plots of 2011 versus 2002. The first plot is all the data; the second plot exlucdes data points that have 0 as their reported income.


```r
par(mfrow = c(1, 2))
FSGRINC.density.2011 <- density(snap_data_frames[[2011]]$FSGRINC)
FSGRINC.density.2002 <- density(snap_data_frames[[2002]]$FSGRINC)
plot(range(FSGRINC.density.2011$x, FSGRINC.density.2002$x), range(FSGRINC.density.2011$y, 
    FSGRINC.density.2002$y), type = "n", ylab = "Density", xlab = "Gross Countable Income", 
    main = "Density of Gross Countable Income (2011=red, 2002=blue")
lines(FSGRINC.density.2011, col = "red")
lines(FSGRINC.density.2002, col = "blue")

FSGRINCNZ.density.2011 <- density(snap_data_frames[[2011]]$FSGRINC[snap_data_frames[[2011]]$FSGRINC != 
    0])
FSGRINCNZ.density.2002 <- density(snap_data_frames[[2002]]$FSGRINC[snap_data_frames[[2002]]$FSGRINC != 
    0])
plot(range(FSGRINCNZ.density.2011$x, FSGRINCNZ.density.2002$x), range(FSGRINCNZ.density.2011$y, 
    FSGRINCNZ.density.2002$y), type = "n", ylab = "Density", xlab = "Gross Countable Income (No Zeros)", 
    main = "Density of Gross Countable Income (0 excluded) (2011=red, 2002=blue")
lines(FSGRINCNZ.density.2011, col = "red")
lines(FSGRINCNZ.density.2002, col = "blue")
```

![plot of chunk unnamed-chunk-3](figure/unnamed-chunk-3.png) 


Now, lets define some functions to help subset our data across all the data sets:


```r
# Subset all the datasets by column name Returns list that maps 'year':
# column
subset_snap_by_column <- function(colname) {
    dataset <- list()
    for (year in seq(YEAR_MIN, YEAR_MAX)) {
        dataset[[as.character(year)]] <- snap_data_frames[[year]][, colname]
    }
    return(dataset)
}

# Subset all the datasets by column name Returns list that maps 'year':
# column
subset_snap_by_column_and_state <- function(colname, state) {
    dataset <- list()
    for (year in seq(YEAR_MIN, YEAR_MAX)) {
        dataset[[as.character(year)]] <- snap_data_frames[[year]][snap_data_frames[[year]]$STATE == 
            state, colname]
    }
    return(dataset)
}
```


Lets try plotting box plots to see the differences in the summary data across all the years:


```r
par(mfrow = c(1, 2))

# Print boxplot of FSGRINC across all years (zoomed out)
boxplot(subset_snap_by_column("FSGRINC"), ylab = "Final Gross Countable Unit Income", 
    xlab = "Dataset", main = "Distribution of FSGRINC Across All Years \n(Zoomed Out)")

# Print boxplot of FSGRINC across all years (zoomed in)
boxplot(subset_snap_by_column("FSGRINC"), ylab = "Final Gross Countable Unit Income", 
    xlab = "Dataset", main = "Distribution of FSGRINC Across All Years \n(Zoomed In)", 
    ylim = c(0, 1500))
```

![plot of chunk unnamed-chunk-5](figure/unnamed-chunk-5.png) 


This is curious: it seems that at-least the median wages in 2011 were higher than that in 2002. This could be due to many factors: recessions, bursted bubbles, etc. Also note, how the variance is getting wider: the area in the middle 50% of the distribution gets wider by the year.

However, one thing I should take care of is adjusting for inflation. To do so, we need to "adjust all dollar figures so that they are expressed in terms of dollars in that year. Often the base year is chosen to be the current year or the final year of study data"^[5][5] . This can be done using a library in R called _quantmod_. Example of its usage is here^[6][6] .


```r
# install.packages('quantmod')
require("quantmod")
getSymbols("CPIAUCSL", src = "FRED")
```

```
## [1] "CPIAUCSL"
```

```r
avg.cpi <- apply.yearly(CPIAUCSL, mean)

# Create a conversion list where 2011 is the base year
inflation_conversion <- list()
for (year in seq(YEAR_MIN, YEAR_MAX)) {
    inflation_conversion[[year]] <- as.numeric(avg.cpi["2011"])/as.numeric(avg.cpi[as.character(year)])
}

# This function will convert x (dollars in year) into dollars in 2011
convert_dollar_to_2011_dollars <- function(x, year) {
    x * inflation_conversion[[year]]
}
```



```r
# Calculate the Adjusted Gross Income if this is the first run
if (!file.exists("snap_data_frames")) {
    for (year in seq(YEAR_MIN, YEAR_MAX)) {
        cbind(snap_data_frames[[year]], ADJ_FSGRINC = sapply(snap_data_frames[[year]]$FSGRINC, 
            convert_dollar_to_2011_dollars, year = year))
    }
}

# Print boxplot of ADJ_FSGRINC across all years (zoomed in)
boxplot(subset_snap_by_column("ADJ_FSGRINC"), ylab = "Final Adjusted Gross Countable Unit Income", 
    xlab = "Dataset", main = "Distribution of Adjusted FSGRINC Across All Years \n(Zoomed In)", 
    ylim = c(0, 1500))
```

![plot of chunk unnamed-chunk-7](figure/unnamed-chunk-7.png) 


Notice, that after adjusting for inflation, the median wage is pretty flat. That means, for people using Food Stamps, increases in the median wage over the past decade were effectively cancelled out by inflation. There is a bit of a bump in 2009 and 2010, which could be attributed to stimulus packages for poorer people. The 25th percentile is also decreasing over time.

Also note, this is for total income (earned and unearned). Lets see if this pattern holds up when looking only at earned income:


```r
par(mfrow = c(2, 2))

# Calculate adjusted earned income
if (!file.exists("snap_data_frames")) {
    for (year in seq(YEAR_MIN, YEAR_MAX)) {
        snap_data_frames[[year]]$ADJ_FSEARN <- sapply(snap_data_frames[[year]]$FSEARN, 
            convert_dollar_to_2011_dollars, year = year)
    }
}

# Print boxplot of FSEARN across all years (zoomed in)
boxplot(subset_snap_by_column("FSEARN"), ylab = "Final Gross Earned Income", 
    xlab = "Dataset Year", main = "Distributions of FSEARN \n(Zoomed In)", ylim = c(0, 
        1000))

# Print boxplot of FSEARN > 0 across all years (zoomed in)
plots <- list()
for (year in seq(YEAR_MIN, YEAR_MAX)) {
    plots[[as.character(year)]] <- snap_data_frames[[year]][snap_data_frames[[year]]$FSEARN > 
        0, "FSEARN"]
}
boxplot(plots, ylab = "Final Gross Earned Income", xlab = "Dataset Year", main = "Distribution of FSEARN != 0")

# Print boxplot of ADJ_FSEARN across all years (zoomed in)
boxplot(subset_snap_by_column("ADJ_FSEARN"), ylab = "Final Adjusted Gross Earned Income", 
    xlab = "Dataset Year", main = "Distribution of Adjusted FSEARN \n(Zoomed In)", 
    ylim = c(0, 1000))

# Print boxplot of ADJ_FSEARN != 0 across all years (zoomed in)
plots <- list()
for (year in seq(YEAR_MIN, YEAR_MAX)) {
    plots[[as.character(year)]] <- snap_data_frames[[year]][snap_data_frames[[year]]$ADJ_FSEARN > 
        0, "ADJ_FSEARN"]
}
boxplot(plots, ylab = "Final Adjusted Gross Earned Income", xlab = "Dataset Year", 
    main = "Distribution of Adjusted FSEARN != 0 \n(Zoomed In)")
```

![plot of chunk unnamed-chunk-8](figure/unnamed-chunk-8.png) 

```r
par(mfrow = c(1, 1))
```


Out of curiosity, what percentage of units reported having 0 earned or total income?


```r
par(mfrow = c(1, 2))

# Earned Income
percent_no_earned_income <- list()
for (year in seq(YEAR_MIN, YEAR_MAX)) {
    percent_no_earned_income[[as.character(year)]] <- length(snap_data_frames[[year]][snap_data_frames[[year]]$FSEARN == 
        0, "FSEARN"])/length(snap_data_frames[[year]][, "FSEARN"])
}
plot(seq(YEAR_MIN, YEAR_MAX), percent_no_earned_income, xlab = "Year", ylab = "Percentage", 
    main = "Percentage of Units Reporting No Earned Income")
lines(seq(YEAR_MIN, YEAR_MAX), percent_no_earned_income, "b")

# Total income
percent_no_income <- list()
for (year in seq(YEAR_MIN, YEAR_MAX)) {
    percent_no_income[[as.character(year)]] <- length(snap_data_frames[[year]][snap_data_frames[[year]]$FSGRINC == 
        0, "FSGRINC"])/length(snap_data_frames[[year]][, "FSGRINC"])
}
plot(seq(YEAR_MIN, YEAR_MAX), percent_no_income, xlab = "Year", ylab = "Percentage", 
    main = "Percentage of Units Reporting No Income")
lines(seq(YEAR_MIN, YEAR_MAX), percent_no_income, "b")
```

![plot of chunk unnamed-chunk-9](figure/unnamed-chunk-9.png) 


Now lets look at Unearned Income:


```r
par(mfrow = c(2, 2))

# Calculate adjusted unearned income
if (!file.exists("snap_data_frames")) {
    for (year in seq(YEAR_MIN, YEAR_MAX)) {
        snap_data_frames[[year]]$ADJ_FSUNEARN <- convert_dollar_to_2011_dollars(snap_data_frames[[year]]$FSUNEARN, 
            year)
    }
}

# Print boxplot of FSUNEARN across all years (zoomed in)
boxplot(subset_snap_by_column("FSUNEARN"), ylab = "Final Gross Countable Unearned Income", 
    xlab = "Dataset Year", main = "Distribution of FSUNEARN \n(Zoomed In)", 
    ylim = c(0, 1000))

# Print boxplot of FSUNEARN > 0 across all years (zoomed in)
plots <- list()
for (year in seq(YEAR_MIN, YEAR_MAX)) {
    plots[[as.character(year)]] <- snap_data_frames[[year]][snap_data_frames[[year]]$FSUNEARN > 
        0, "FSUNEARN"]
}
boxplot(plots, ylab = "Final Gross Countable Unearned Income", xlab = "Dataset Year", 
    main = "Distribution of FSUNEARN != 0", ylim = c(0, 1000))

# Print boxplot of ADJ_FSUNEARN across all years (zoomed in)
boxplot(subset_snap_by_column("ADJ_FSUNEARN"), ylab = "Final Adjusted Gross Unearned Income", 
    xlab = "Dataset Year", main = "Distribution of Adjusted FSUNEARN \n(Zoomed In)", 
    ylim = c(0, 1000))

# Print boxplot of ADJ_FSUNEARN != 0 across all years (zoomed in)
plots <- list()
for (year in seq(YEAR_MIN, YEAR_MAX)) {
    plots[[as.character(year)]] <- snap_data_frames[[year]][snap_data_frames[[year]]$ADJ_FSUNEARN > 
        0, "ADJ_FSUNEARN"]
}
boxplot(plots, ylab = "Final Adjusted Gross Unearned Income", xlab = "Dataset Year", 
    main = "Distribution of Adjusted FSUNEARN != 0 \n(Zoomed In)", ylim = c(0, 
        1000))
```

![plot of chunk unnamed-chunk-10](figure/unnamed-chunk-10.png) 


### Plot Rent

After adjusting for inflation, reported Rent values seem to stay steady (the median and 25th/75th percentile range stay pretty flat). The increases you see in the top two graphs seem to be due largely to inflation. There maybe be many reasons for this, which a domain expert could shine some light on. One reason that comes to mind is that many people who are on Food Stamps may very well also be in rent-controlled apartments, or otherwise get subsidies for their rent expenses.



```r
par(mfrow = c(2, 2))
# Print boxplot of RENT across all years (zoomed out)
boxplot(subset_snap_by_column("RENT"), ylab = "Reported Rent", xlab = "Dataset Year", 
    main = "Distribution of Reported Rent \n(Zoomed Out)", ylim = c(0, 3500))

# Print boxplot of RENT across all years (zoomed in)
boxplot(subset_snap_by_column("RENT"), ylab = "Reported Rent", xlab = "Dataset Year", 
    main = "Distribution of Reported Rent \n(Zoomed In)", ylim = c(0, 1200))

# Calculate adjusted rent
if (!file.exists("snap_data_frames")) {
    for (year in seq(YEAR_MIN, YEAR_MAX)) {
        snap_data_frames[[year]]$ADJ_RENT <- convert_dollar_to_2011_dollars(snap_data_frames[[year]]$RENT, 
            year)
    }
}

# Plot the adjusted rent
boxplot(subset_snap_by_column("ADJ_RENT"), ylab = "Adjusted Reported Rent", 
    xlab = "Dataset Year", main = "Distribution of Adjusted Rent \n(Zoomed Out)", 
    ylim = c(0, 3000))

# Plot the adjusted rent but zoomed
boxplot(subset_snap_by_column("ADJ_RENT"), ylab = "Adjusted Reported Rent", 
    xlab = "Dataset Year", main = "Distribution of Adjusted Rent \n(Zoomed In)", 
    ylim = c(0, 1200))
```

![plot of chunk unnamed-chunk-11](figure/unnamed-chunk-11.png) 


### Ratio of Rent to Income

Lets calculate the ratio of the _RENT_ column and the _FSGRINC_ column and plot the resulting boxplots:


```r
par(mfrow = c(1, 1))
if (!file.exists("snap_data_frames")) {
    for (year in seq(YEAR_MIN, YEAR_MAX)) {
        snap_data_frames[[year]]$RENT_INC_RATIO <- (snap_data_frames[[year]]$RENT + 
            1)/(snap_data_frames[[year]]$FSGRINC + 1)
    }
}

# Boxplot for these ratios
boxplot(subset_snap_by_column("RENT_INC_RATIO"))
```

![plot of chunk unnamed-chunk-12](figure/unnamed-chunk-12.png) 


Ok, thats a bit ugly. This is due to a lot of extreme values due to either no reported rent or income. Lets zoom in a bit to see the IQR:


```r
# Lets trim the output for reasonable values
stats <- boxplot(subset_snap_by_column("RENT_INC_RATIO"), ylim = c(0, 2))
```

![plot of chunk unnamed-chunk-13](figure/unnamed-chunk-13.png) 


It does seem that over time, this ratio is increasing. We can see this by plotting the median value over time:


```r
# Plot the median ratio over time
plot(seq(YEAR_MIN, YEAR_MAX), stats$stats[3, ], xlab = "Dataset Year", ylab = "Median Ratio", 
    main = "Median Ratio of Rent to Gross Income")
lines(seq(YEAR_MIN, YEAR_MAX), stats$stats[3, ], "b")
```

![plot of chunk unnamed-chunk-14](figure/unnamed-chunk-14.png) 


If we look at the distributions for income, we see that 25th percentile (the bottom of the box in the boxplots) decreases over time. Theore, the IQR is generally spreading downwards. The rent boxplots, however, seem to stay steady. This would insinutate that the ratio of rent to income is increasing due to lower total income, not changing values of rent.

For completion, here is the percentage of data points (per year) that are 'outliers' in the boxplots (approximately 6% over all datasets):


```r
percent_outliers <- sapply(seq(YEAR_MIN, YEAR_MAX), function(year) {
    length(snap_data_frames[[year]]$RENT_INC_RATIO[snap_data_frames[[year]]$RENT_INC_RATIO > 
        stats$stats[5, year - 2001]])/length(snap_data_frames[[year]]$RENT_INC_RATIO)
})
plot(seq(YEAR_MIN, YEAR_MAX), percent_outliers, ylab = "Percentage", xlab = "Dataset", 
    main = "Percentage of Data Points that are Outliers")
lines(seq(YEAR_MIN, YEAR_MAX), percent_outliers, "b")
```

![plot of chunk unnamed-chunk-15](figure/unnamed-chunk-15.png) 


### Map of Change in Median Ratio

Here we can sub-set the data by state, and see the change in rent-to-income ratio for that state only. Here is an example for New York:


```r
plot_ratio_by_state <- function(state) {
    boxplot(subset_snap_by_column_and_state("RENT_INC_RATIO", state), ylab = "Rent / Income", 
        xlab = "Dataset Year", main = paste("Distribution of Rent / Income Ratio in", 
            state, " \n(Zoomed In)"), ylim = c(0, 2))
}

plot_ratio_by_state(36)
```

![plot of chunk unnamed-chunk-16](figure/unnamed-chunk-161.png) 

```r

states <- unique(snap_data_frames[[2011]]$STATE)

state_change <- list()
for (state in states) {
    x <- median(snap_data_frames[[2011]]$RENT_INC_RATIO[snap_data_frames[[2011]]$STATE == 
        state])
    y <- median(snap_data_frames[[2002]]$RENT_INC_RATIO[snap_data_frames[[2002]]$STATE == 
        state])
    state_change[[state]] <- x - y
}

state_median <- list()
for (state in states) {
    state_median[[state]] <- median(snap_data_frames[[2011]]$RENT_INC_RATIO[snap_data_frames[[2011]]$STATE == 
        state])
}

library(maps)

# make first polygon have color 1, second 2, etc.
x <- unlist(state_change)
x_norm <- (x - min(x))/(max(x) - min(x))
col_fun <- colorRamp(c("blue", "red"))
rgb_cols <- col_fun(x_norm)
colors <- rgb(rgb_cols, maxColorValue = 256)

map("state", fill = TRUE, col = colors)
title("Change Median Ratio of Rent to Income from 2002 to 2011")
```

![plot of chunk unnamed-chunk-16](figure/unnamed-chunk-162.png) 

```r

# make first polygon have color 1, second 2, etc.
x <- unlist(state_median)
x_norm <- (x - min(x))/(max(x) - min(x))
col_fun <- colorRamp(c("blue", "red"))
rgb_cols <- col_fun(x_norm)
colors <- rgb(rgb_cols, maxColorValue = 256)

map("state", fill = TRUE, col = colors)
title("Ratio of Rent to Income, 2011")
```

![plot of chunk unnamed-chunk-16](figure/unnamed-chunk-163.png) 




## Potential Flaws

Some questions come to mind during the analysis:

* Might be doing inflation corrcetion incorrectly. I think I have it right, but there is no well-defined way to calculate inflation (some use CPI, some use Chained CPI, some use a different metric)
* In order to deal with 0 values in both reported rent and the raw and calculated gross income, I added a 1 to both numerator and denominator. Justification: (x+1)/(y+1) is approximately (x/y), and prevents infinite numbers. If the reported rent is 0, then the calculation will come up with a very small value.

## Conclusions and Future Work

The conclusion is that it does seem that over the past decade, users who receieve Food Stamps have an increasing ratio of rent to gross income. 

Future work would not only look at this SNAP data from many different views, but also integrate other government data (Census data, economic health metrics, etc) for deeper insights. For example, there is an 'Employment Status' column which can be used to see if SNAP beneficiaries are working less or more over time.

## Lessons

* Domain knowledge is crucial to undertsanding whats going on with the data
* Playing with the data by plotting different dimenions in different ways, is invaluable
* These analyses take longer than expected


## Useful Links

* [SNAP Wikipedia Page](http://en.wikipedia.org/wiki/Supplemental_Nutrition_Assistance_Program)
* [ZH Link](http://www.zerohedge.com/news/2013-12-09/rent-too-damned-high)



[1]: http://hostm142.mathematica-mpr.com/fns/2011/tech%20doc%202011.pdf_2011 "SNAP Data Document"
[2]: TODO: fill this in "Origin Site for Data"
[3]: http://presbrey.mit.edu/PyDTA#export_to_CSV "Python Stata (DTA) Module"
[4]: http://soda.pop.psu.edu/cgi-bin/broker?_SERVICE=sodapop&_PROGRAM=sodaprog.extract_function.sas&coll=snap&ds=qcfy2011 "Penn State Mirror Of Data"
[5]: http://www.herc.research.va.gov/resources/faq_a03.asp "Adjusting for Inflation"
[6]: http://stackoverflow.com/questions/12590180/inflation-adjusted-prices-package "Using R to Adjust for Inflation"
