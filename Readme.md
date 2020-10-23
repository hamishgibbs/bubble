# :droplet: Bubble 

CLI tool for scafoflding research projects

Python CLI with click

### Motivation:
* I don't like doing repetitive things 
* I don't test my code very often
* I am slow to add Makefile targets
* I use absolute file paths

### Features:

* Scaffold Python and R files for easy input/output and interactive coding
* support to update existing projects with new formats
* parse a bubble template file to generate a makefile target and insert in an existing makefile 
* generate corresponding testing infrastructre for all functions in a file
	* using testthat or pytest

### Usage:
``` {shell} 
bubble process.R -csv -test
```

`-csv`: generate a template for outputting a csv file  
`-png`: generate a template for outputting a png image  
`-module`: generate a template for a module  
`-test`: set up a corresponding test file  


