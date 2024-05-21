# Information Retrieval System - Evaluator

## Project Target

Create an IR system evaluator from a predetermined dataset. Evaluation is based on MAP (Mean Average Precision).

## Features

1. Read a document dataset
2. Evaluate TF-IDF-Norm values of documents
3. Evaluate TF-IDF-Norm values of query
4. Evaluate MAP values of queries

## Structure

-   src/irsystem

    -   base

        Base class, most logic lives here

        -   choices : List of choices, i.e. conversion modes
        -   reader : Base reader class, reads a document collection to memory
        -   converter : Converts a TF table based on conversion modes

    -   adi

        ADI test collection

        -   reader : Child class from base/reader for ADI test collection
        -   data : ADI data collection files

## How To: Setup

1. Create an environment
    ```
    python -m venv venv
    ```
2. Go to src/irsystem as the main project source folder
    ```
    cd .\src\irsystem
    ```
3. Install required packages
    ```
    pip install -r .\requirements.txt
    ```
