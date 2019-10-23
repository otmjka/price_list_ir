conda activate syn-ir

## deps:

- pandas
- xlrd
- psycopg2


1. load ISKUs from sqlite
2. update ISKUs, new way, get from `unificated_nomenclature` table
  - fill needed fields: `tn`, `lek`, `dosage`, `count`, `company` from sources *graphql*
connect to sqlite
load en
build row_num/en_uuid index
load price
simple tokenize

## TODO:

upload file
hash to file
make config
logging

