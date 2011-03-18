#!/usr/bin/Rscript
library(rjson)

x <- list( varA = 5 )
sink('routput')
cat(toJSON(x))
sink()