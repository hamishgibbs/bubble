suppressPackageStartupMessages({
  require(tidyverse)
})

# source('file')

if(interactive()){
  .args <-  c('input',
              'output')
} else {
  .args <- commandArgs(trailingOnly = T)
}





write_csv(res, tail(.args, 1))