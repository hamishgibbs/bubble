suppressPackageStartupMessages({
  require(tidyverse)
  require(ggplot)
})

# source('file')

if(interactive()){
  .args <-  c('input',
              'output')
} else {
  .args <- commandArgs(trailingOnly = T)
}




ggsave(tail(.args, 1), 
       p,
       width = 8.5, height = 6,
       units = 'in')

ggsave(gsub('.png', '.pdf', tail(.args, 1)), 
       p,
       width = 8.5, height = 6,
       units = 'in',
       useDingbats = F)