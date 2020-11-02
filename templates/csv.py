"""
TITLE.py

Script to ...

"""

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
