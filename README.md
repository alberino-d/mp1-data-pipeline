# MP1 Data Pipeline
This project implements an end-to-end pipeline that loads, validates, cleans, and saves structured data using configurable settings. The pipeline loads CSV or other file formats and reads its processing and validation settings from `config/config.yaml`. The `src/data_loaders.py` module handles the loading of data, and the `src/data_validator.py` module checks the existence of required columns and removes rows containing non-numeric values in numeric columns. The `src/data_processor.py` module cleans the data by removing entries with duplicate values, handling missing values, and identifying outliers. The `src/data_output.py` module saves the cleaned data as a CSV file, and the `src/utils.py` module sets up the logging configuration and validates the input file. `src/__init__.py` makes the module functions available to the pipeline.py script, which coordinates all the modules. The `/fixtures` directory contains all the sample data files, and the `/output` directory houses the cleaned output data.

## Running the Pipeline
Activate your virtual environment and run the following command from the repository root:
```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```
The pipeline logs its steps through loading, validation, and processing, then saves the cleaned data to `output/clean.csv` while printing a report summarizing the results of the cleaning process.
