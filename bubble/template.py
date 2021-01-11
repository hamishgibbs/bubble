def templates():
    '''Function to access dict of available templates'''

    return(
        {'r': r(),
         'py': py(),
         'makefile': makefile()}
    )


def r():
    '''R file template'''

    return(

        """
        # *** bubble make ***

        # Script to ...

        # Load libraries
        suppressPackageStartupMessages({
          require(tidyverse)
          require(ggplot2)
        })

        # Source modules
        # source("file")

        # *** bubble input start ***
        # Define args interactively or accept commandArgs
        if(interactive()){
          .args <-  c("input",
                      "output")
        } else {
          .args <- commandArgs(trailingOnly = T)
        }
        # *** bubble input end ***
        """

    )


def py():
    '''Python file template'''

    return (
        """
        # *** bubble make ***

        '''
        TITLE.py

        Script to ...

        '''

        # Load libraries
        import __main__ as main
        import sys

        # *** bubble input start ***
        # Define args interactively or accept commandArgs
        if not hasattr(main, "__file__"):
            argv = ["code",
                    "input",
                    "output"]
        else:
            argv = sys.argv
        # *** bubble input end ***"""
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
