Description of Project
======================

## Summary 

_Demonstrates business value.  Describe how “customer” (company or organization or society) currently operates/decides, and how this data will be helpful (in making better decisions, providing insights, taking costs out of system, improving asset utilization, etc.)_

"The Food Stamp program (The Supplemental Nutrition Assistance Program), provides financial assistance for purchasing food to low- and no-income people living in the U.S. It is a federal aid program, administered by the U.S. Department of Agriculture, though benefits are distributed by individual U.S. states. They can be used to purchase any prepackaged edible foods, regardless of nutritional value (e.g. soft drinks and confections). Hot foods (such as those found in a supermarket deli) are ineligible, as well as items in fast food restaurants and similar retail settings." - http://en.wikipedia.org/wiki/Supplemental_Nutrition_Assistance_Program

"The characteristics of SNAP households and households’ level of participation in SNAP change
over time in response to economic and demographic trends and legislative adjustments to program
rules. To measure the effect of these changes on SNAP, FNS relies on data from the SNAP Quality
Control (SNAP QC) database. This database is an edited version of the raw datafile of monthly case
reviews conducted by State SNAP agencies to assess the accuracy of eligibility determinations and
benefit calculations for each State’s SNAP caseload.

The data design document describes how the raw data are cleaned and edited to create the SNAP QC database. It also describes how the QC Minimodel — one of FNS’ SNAP microsimulation models — uses the SNAP QC database to simulate the impact of various reforms to SNAP on current SNAP participants."

## Hypothesis

I'll be invetsigating if there is a trend over time for SNAP receipients to pay more rent as a percentgae of their income. This trend can be broken down over many demographies, like where someone lives, their race or age. My suspicion is that those receiving SNAP benefits pay more of their income go to rent as time goes on, especially in bigger cities.

The data from any given year has samples of data that are reported to the federal government by the individual states. Documentation from the Dept of Agriculture describes the process each state goes through to provide the data, from making sure populations are not oversampled, and how many samples to submit based on state population. The data set provides two columns, one for reported rent and reported total income, which can be used to calculate the percentage of income going to rent for any sample. I'm hoping that this can be graphed over time.

## Useful Links

* [SNAP Wikipedia Page](http://en.wikipedia.org/wiki/Supplemental_Nutrition_Assistance_Program)
* [SNAP Data Worksheet](http://hostm142.mathematica-mpr.com/fns/2011/tech%20doc%202011.pdf_2011)
* [PyDTA](http://presbrey.mit.edu/PyDTA#export_to_CSV)
* [ZH Link](http://www.zerohedge.com/news/2013-12-09/rent-too-damned-high)

## TODO:

* Create decision tree trying to predict calculated column
* Create map of USA showing scale of average % of income spent on rent
* Show some state-level data

## Methodology

### Load Data


```r
# Set the correct path
setwd("~/Code/Masters/IS607/Project/")

# Load 2011 SNAP Data
if (!file.exists("df_2011")) {
    df_2011 <- read.csv("snap/data_2011.csv")
    save(list = "df_2011", file = "df_2011")
} else {
    load("df_2011")
}
```


### Plot Histogram of wages


```r
hist(df_2011$wages1[df_2011$wages1 != 0])
```

![plot of chunk unnamed-chunk-2](figure/unnamed-chunk-21.png) 

```r
plot(density(df_2011$wages1[df_2011$wages1 != 0]))
```

![plot of chunk unnamed-chunk-2](figure/unnamed-chunk-22.png) 


### Plot SSI1


```r
hist(df_2011$ssi1[df_2011$ssi1 != 0], breaks = 50)  # Interesting spike
```

![plot of chunk unnamed-chunk-3](figure/unnamed-chunk-31.png) 

```r
plot(density(df_2011$ssi1[df_2011$ssi1 != 0]))
```

![plot of chunk unnamed-chunk-3](figure/unnamed-chunk-32.png) 


Things to note:
* There is a spike that is unexpected here. Why? Data artifact, or part of SSI policy?

### Plot Rent


```r
hist(df_2011$rent, breaks = 50)
```

![plot of chunk unnamed-chunk-4](figure/unnamed-chunk-41.png) 

```r
hist(df_2011$rent[df_2011$rent != 0], breaks = 50)
```

![plot of chunk unnamed-chunk-4](figure/unnamed-chunk-42.png) 


## Conclusions and Future Work
