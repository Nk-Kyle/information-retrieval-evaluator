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
        -   converter : Converts a TF table based on conversion modes
        -   parser : parses string to tokens, including stemming
        -   query : Base query reader, reads a query collection to memory
        -   reader : Base document reader class, reads a document collection to memory
        -   relevance : Relevance document reader class, reads a relevance measure of query and corresponding relevant document to memory
        -   irs : IR System Wrapper, main class to run ir evaluation

    -   adi, cacm, cran, med, npl, time

        ADI, CACM, CRAN, MED, NPL, TIME test collection implementation. Implements methods defined in base classes based on test collection structures.

        -   query : Child class from base/query for specific test collection
        -   reader : Child class from base/reader for specific test collection
        -   relevance : Child class from base/relevance for specific test collection
        -   data : Specific data collection files

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
