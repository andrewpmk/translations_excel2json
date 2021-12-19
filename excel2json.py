#!/usr/bin/env python3

import json
import os
import pandas

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
            if langcode not in output:
                output[langcode] = {}
            output[langcode][resourcekey] = value

def main():
    excel = pandas.read_excel("Vaccine Hunters Canada Translations.xlsx")

    if not resourcekeycolumn in excel:
        raise ValueError("Resource key column not found in Excel file")

    for index, row in excel.iterrows():
        processrow(index, row)

    saveoutput()

def saveoutput():
    for langcode in output.keys():
        if not os.path.exists(langcode):
            os.makedirs(langcode)
        f = open(langcode + "/translation.json", "w", encoding="utf-8")
        # Pretty print JSON with 4 character indent
        jsondata = output[langcode]
        json.dump(jsondata, f, indent=4, sort_keys=True, ensure_ascii=False)
        f.close()

if __name__ == "__main__":
    main()