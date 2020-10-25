# Script to ...

# Load libraries
suppressPackageStartupMessages({
  require(tidyverse)
})

# Load environment variables from .env file
dotenv::load_dot_env(file = ".env")

# Source modules
# source('file')

# Define args interactively or accept commandArgs
if(interactive()){
  .args <-  c('input',
              'output')
} else {
  .args <- commandArgs(trailingOnly = T)
}

# -- Process data here --


# Save csv result
write_csv(res, tail(.args, 1))
