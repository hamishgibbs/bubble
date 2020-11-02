# Script to ...

# Load libraries
suppressPackageStartupMessages({
  require(tidyverse)
  require(ggplot2)
})

# Load environment variables from .env file
dotenv::load_dot_env(file = ".env")

# Source modules
# source("file")

# Define args interactively or accept commandArgs
if(interactive()){
  .args <-  c("input",
              "output")
} else {
  .args <- commandArgs(trailingOnly = T)
}

# -- Create plot here --


# Save png image
ggsave(tail(.args, 1),
       p,
       width = 8.5, height = 6,
       units = "in")

# Save idenfitcal pdf image
ggsave(gsub(".png", ".pdf", tail(.args, 1)),
       p,
       width = 8.5, height = 6,
       units = "in",
       useDingbats = F)
