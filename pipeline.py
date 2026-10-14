"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config.yaml
    python pipeline.py --input fixtures/sample_data.csv --output output/results.json --config config.yaml --verbose
"""

import argparse
import logging
import sys
from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)


logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Processes CSV/JSON files.")

    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to the input file"
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to YAML configuration file"
    )

    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Path to the output file"
    )

    # parser.add_argument(
    #     "--format",
    #     choices=["csv", "json"],
    #     default="csv",
    #     help="Output format"
    # )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed DEBUG messages"
    )

    return parser.parse_args()


def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)

    logger.debug(f"Arguments parsed: input={args.input}, output={args.output}, config={args.config}")

    if not validate_input(args.input):
        sys.exit(1)

    if not validate_input(args.config):
        sys.exit(1)

    try:
        input_data = load_data(args.input)
        config_data = load_data(args.config)
    except ValueError as error:
        logger.error(f"Error loading data or configuration: {error}")
        sys.exit(1)

    required_columns = config_data["validation"]["required_columns"]
    numeric_columns = config_data["validation"]["numeric_columns"]

    rows_before_validation = len(input_data)

    try:
        input_data = validate_dataframe(input_data, required_columns, numeric_columns)
    except ValueError as error:
        logger.error(f"Data validation failed: {error}")
        sys.exit(1)

    logger.info(f"Validation complete: From {rows_before_validation} to {len(input_data)} rows.")

    og_input_data = input_data.copy()

    try:
        processed_data = process_data(input_data, config_data)
    except ValueError:
        logger.error(f"Data processing failed: {error}")
        sys.exit(1)

    logger.info(f"Processing complete: From {len(og_input_data)} to {len(processed_data)} rows.")

    output_path = save_data(processed_data, args.output)
    logger.info(f"Saved cleaned data to {output_path}")

    cleaning_report = create_cleaning_report(og_input_data, processed_data)

    print("\nCleaning Report:")
    print(cleaning_report)




if __name__ == "__main__":
    main()
