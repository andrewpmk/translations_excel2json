#!/usr/bin/env python3

import argparse
import json
import os
import pandas
from pathlib import Path

# Column containing resource key
resourcekeycolumn = "Resource key"

# Resource keys to ignore
resourcekeyignore = ["Copy this row to Google Translate"]

# Columns containng translations
columns = {
    "English": "en",
    "French": "fr",
    "Arabic": "ar",
    "Bengali": "bn",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Croatian": "hr",
    "German": "de",
    "Hebrew": "he",
    "Hungarian": "hu",
    "Italian": "it",
    "Japanese": "ja",
    "Persian (Farsi)": "fa",
    "Polish": "pl",
    "Portuguese (Brazil)": "pt",
    "Romanian": "ro",
    "Russian": "ru",
    "Serbian": "sr",
    "Spanish (Latin America)": "es",
    "Tagalog": "tl",
    "Tamil": "ta",
    "Turkish": "tr",
    "Vietnamese": "vi"
}

output = {}

# Process row of Excel file
def processrow(index, row):
    resourcekey = row[resourcekeycolumn] # column containing resource keys
    if resourcekey in resourcekeyignore:
        return # Ignore resource keys in resourcekeyignore
    for column in columns.keys(): # iterate through columns
        if column in row:
            langcode = columns[column] # Get corresponding language code
            if (langcode == ""):
                raise ValueError("Invalid language code")
            value = row[column] # Get value
            if pandas.isna(value): # Ignore nan
                continue
            # Add language code to output
            if langcode not in output:
                output[langcode] = {}
            # Add resource key to output
            output[langcode][resourcekey] = value

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input Excel file")
    parser.add_argument("output", help="Output directory to place .json files")
    args = parser.parse_args()

    excel = pandas.read_excel(args.input)

    if not resourcekeycolumn in excel:
        raise ValueError("Resource key column not found in Excel file")

    for index, row in excel.iterrows():
        processrow(index, row)

    saveoutput(args.output)

def saveoutput(outputdir):
    for langcode in output.keys():
        # Remove hyphens because zh-CN and zh-TW are stored in zhCN and zhTW respectively
        langcode_path = str(langcode).replace("-", "")
        directory = os.path.join(outputdir, langcode_path)
        # Create directory if it doesn't exist
        Path(directory).mkdir(parents=True, exist_ok=True)
        f = open(os.path.join(directory, "translation.json"), "w", encoding="utf-8")
        # Pretty print JSON with 4 character indent
        jsondata = output[langcode]
        # Save JSON to file
        json.dump(jsondata, f, indent=4, sort_keys=True, ensure_ascii=False)
        f.close()

if __name__ == "__main__":
    main()