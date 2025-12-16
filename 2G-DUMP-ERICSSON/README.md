# 2G Ericsson Database Project

This project focuses on the 2G Ericsson database using the **AllParameters** dataset.  
For example purposes, we use the file `AllParameters_15nov`, which is located in the `data/` directory.  

The workflow includes:
1. Processing and cleaning the raw GSM data.
2. Importing the processed data into a **MongoDB** database.
3. Preparing the data for analysis and reporting.

## Data
- **Source:** Ericsson 2G network
- **Sample File:** `AllParameters_15nov`
- **Location:** `data/` folder

## Requirements
- Python 3.x
- pandas
- numpy
- pymongo
- pathlib

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/sohrabimaryam88-droid/GSM
   cd gsm