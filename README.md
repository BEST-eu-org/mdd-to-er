# Makumba Data Definition to Entity-Relationship diagram

A tool to extract an Entity-Relationship (ER) diagram from Makumba Data Definition (MDD) files.

![Example image](https://github.com/samupino/mdd-to-er/blob/master/example/example_image.png)

(See the example for the details)

## Setup

#### Requirements

- Unix operative system
- Python 3
- Virtualenv package

#### Steps

1. Create a virtual environment:

`python3 -m venv env`

2. Source the virtual environment:

`source env/bin/activate`

3. Install grapviz:

`pip install graphviz`

## Run

Source the virual environment (if not done already):

`source env/bin/activate`

Run the script to generate the drawing code:

`python mdd2er.py <path-to-mdds-directory> [depth-limit (default=10)]`
