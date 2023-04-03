<a href="https://www.thecocktaildb.com"><img src="https://thecocktaildb.com/images/logo.png"></a><br>

# Cocktail // Case Study

## Description

  The following case study had been handed over during a job application process.


#### C a s e :

  ——
  <p>
  <ol type="1">
    <li><p>&nbspCreate a python script which downloads as much drinks as possible from following page: https://www.thecocktaildb.com/api.php</p></li>
    <li><p>&nbspCreate a relational database in sqlite for the downloaded data, under the assumption that your database could grow to over 10 million datasets.</p></li>
    <li><p>&nbspExtend your script (from point 1) to insert the data in your database. Please insert just data which has German instructions.</p></li>
    <li><p>&nbsp<u>Which are the SQL queries for following questions:</p></li>
    <t>
      <ol type="A">
        <li>&nbspWhich alcoholic drinks can be mixed with lemon and whiskey?</li>
        <li>&nbspWhich drink(s) can be mixed with just 15g of Sambuca?</li>
        <li>&nbspWhich drink has the most ingredients?</li>
      </ol>
    </t>
  </ol>
  </p>
  ——



## Getting Started

### Dependencies

  In order to run/execute the solution the following dependencies need to be considered and resolved:
  
  The script was developed in Python version 3.10.10. Check if you have the same version (or higher) in your environment or find an applicable online environment to run the script.
  
  * Checking the python version in your environment can be managed with the following command:
        
        $ python --version
  * In case you don't have python installed on your computer please download it from Python's [official website](https://www.python.org/downloads/).
       
  * The below Python libraries are used in the project:

    `requests`
    
    `string`
    
    `json`
    
    `random`
    
    `sqlite3`
    
    <b>NOTE:</b> Please be aware that `requests` is a non standard python library you need to install it separately see the [Installing](#installing) section below.



### Installing

  * Download the [cocktail_case_study.py](https://github.com/pszly/meinestadt-case-study/blob/meinestadt-case-study/cocktail_case_study.py) file on your computer.
  * Make sure to install `requests` library in python w/ pip. In case you don't have pip installed on your environment refer the official [pip documentation](https://pip.pypa.io/en/stable/installation/). This project uses `requests` library [version 2.28.2](https://pypi.org/project/requests/2.28.2/).
    
        $ python -m pip install requests==2.28.2



### Executing

   Run the program with the following command in command line:
  
  * Locate cocktail_case_study.py file in command line then run the followin command in the parent folder.

         $ python cocktail_case_study.py



## Help

   In case of any questions contact the author below.



## Author

   Peter Szalay  
   [peter@proniq.eu](mailto:peter@proniq.eu)


## Version History

  * v0.1  [ 2023.04.03. ] Readme.md added
  * v1.0  [ 2023.04.03. ] Initial Release
  * v1.1  [ 2023.04.03. ] Script modified


## Data Source

   <a href="https://www.thecocktaildb.com"><img src="https://thecocktaildb.com/images/logo.png"></a><br>
   
   [TheCocktailDB](https://www.thecocktaildb.com/)
