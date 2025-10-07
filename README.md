# Intelliverse Attractions  

This project demonstrates a sample dataset of tourist attractions worldwide and provides Python scripts to generate and validate the data.  

## Contents
- **generate.py** → Generates the dataset in JSON format  
- **quick_check.py** → Validates the dataset and prints sample records with year distribution  
- **attractions_recent.json** → The generated dataset file  

## Usage
1. Generate a new dataset:
   python generate.py
2. Run quick validation:
   python quick_check.py

## Example Output
Total records: 100  
Records with missing fields: 0  
Records satisfying year condition: 1200  
Sample record: { 'name': 'Calgary Green Roof Gardens', ... }  
Year distribution: {'2021': 229, '2022': 238, '2023': 239, '2024': 243, '2025': 251}

## Requirements
- Python 3.9+  
- Built-in libraries: json, re, collections

## License
MIT License  



