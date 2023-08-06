# Qualifyr

## Installation
```
python setup.py install
```

## Tests
```
python setup.py test
``` 

## Test in dev
  - clone repo
  - cd into directory
  - to see pass result run `qualifyr -y tests/test_data/pass_conditions.yml -q tests/test_data/quast_valid.txt  -f tests/test_data/fastqc_valid.txt`
  - to see fail result run `qualifyr -y tests/test_data/fail_conditions.yml -q tests/test_data/quast_valid.txt  -f tests/test_data/fastqc_valid.txt`