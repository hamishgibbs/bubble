def templates():
    '''Function to access dict of available templates'''

    return(
        {'R': {'csv': r_csv,
               'png': r_png,
               'module': r_module,
               'makefile': makefile,
               'dockerfile': r_dockerfile},
        'PYTHON': {'csv': py_csv,
                   'png': py_png,
                   'module': py_module,
                   'makefile': makefile,
                   'dockerfile': py_dockerfile}}
    )


def r_png():
    '''R PNG template'''

    return(

        """# Script to ...

        # Load libraries
        suppressPackageStartupMessages({
          require(tidyverse)
          require(ggplot2)
        })

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

        # Save identical pdf image
        ggsave(gsub(".png", ".pdf", tail(.args, 1)),
               p,
               width = 8.5, height = 6,
               units = "in",
               useDingbats = F)"""

    )


def r_csv():
    '''R CSV template'''

    return(

        """# Script to ...

        # Load libraries
        suppressPackageStartupMessages({
          require(tidyverse)
        })

        # Source modules
        # source("file")

        # Define args interactively or accept commandArgs
        if(interactive()){
          .args <-  c("input",
                      "output")
        } else {
          .args <- commandArgs(trailingOnly = T)
        }

        # -- Process data here --


        # Save csv result
        write_csv(res, tail(.args, 1))"""

    )


def r_module():
    '''R module template
    Format current f with file name
    '''

    return(
        """# Module to ...

        # Load libraries
        suppressPackageStartupMessages({
          require(tidyverse)
          require(ggplot2)
        })

        # source('file')

        f <- function(x){

          return(x)

        }"""
    )

def r_dockerfile():
    '''R dockerfile template'''

    return(
        """
        FROM rocker/verse:latest

        ADD . /home/rstudio/proj

        WORKDIR /home/rstudio/proj

        RUN Rscript -e "install.packages('tidyverse')"
        """
    )

def py_png():
    '''Python PNG template'''

    return (
        """
        '''
        TITLE.py

        Script to ...

        '''

        # Load libraries
        import __main__ as main
        import sys
        import matplotlib.pyplot as plt
        import seaborn as sns
        from dotenv import load_dotenv

        # Load environment variables from .env file
        load_dotenv(dotenv_path=".env")

        # Define args interactively or accept commandArgs
        if not hasattr(main, "__file__"):
            argv = ["code",
                    "input",
                    "output"]
        else:
            argv = sys.argv


        p.savefig(argv[-1])
        p.savefig(argv[-1].replace(".png", ".pdf"))"""
    )


def py_csv():
    '''Python CSV template'''

    return (
        """
        '''
        TITLE.py

        Script to ...

        '''

        # Load libraries
        import __main__ as main
        import sys
        import pandas as pd
        from dotenv import load_dotenv

        # Load environment variables from .env file
        load_dotenv(dotenv_path=".env")

        # Define args interactively or accept commandArgs
        if not hasattr(main, "__file__"):
            argv = ["code",
                    "input",
                    "output"
            ]
        else:
            argv = sys.argv

        # -- Process data here --


        # Save csv file
        res.to_csv(argv[-1])
        """
    )


def py_module():
    '''Python module template'''

    return(
     """'''
     TITLE.py

     Script to ...

     '''

     import pandas as pd

     def f():
         return(1)
     """
    )


def py_dockerfile():
    '''Python dockerfile template'''

    return(
        """
        # Using slim python 3.8 container
        FROM python:3.8-slim

        COPY requirements.txt ./

        # Install python dependencies
        RUN pip install --no-cache-dir -r requirements.txt

        # Install make
        RUN apt-get update && apt-get install make

        # Set working directory
        WORKDIR /usr/proj

        # Copy all files to container
        COPY . .
        """
    )

def makefile():
    '''R and Python Makefile template'''

    return(
        """# Python interpreter
        PYTHON_INTERPRETER = python3

        # R interpreter
        R_INTERPRETER = /usr/local/bin/Rscript

        # Search for .env file variables
        ifneq (,$(wildcard ./.env))
            include .env
            export
        endif
        """
    )
