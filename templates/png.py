"""
TITLE.py

Script to ...

"""

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
p.savefig(argv[-1].replace(".png", ".pdf"))
