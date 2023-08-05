# nucleopy

[![Python27](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/download/releases/2.7/)
[![Python34](https://img.shields.io/badge/python-3.4-yellow.svg)](https://www.python.org/download/releases/3.4.0/)
[![License](https://img.shields.io/badge/license-Apache%202.0-black.svg)](https://github.com/RK900/nucleopy/blob/master/LICENSE)

Scientific Python library to easily work with nucleotide data. Users can create `DNA` and `RNA` objects and easily manipulate them
for use in scientific programming.
## Author
Rohan Koodli

## To Use
```pip install nucleopy```

See the `examples` folder for example use cases for nucleopy.

### Creating a nucleotide object
```python
r = RNA('AGGCUUUACA')
d = DNA('ATCGGATCCG')
```

### Functions
```python
d.complement() # TAGCCTAGGC
d.isComplement('TAAGCG') # False
r.toDNA() # AGGCTTTACA
```

### RNA-specific functions (requires [ViennaRNA](https://github.com/ViennaRNA/ViennaRNA) installation)
```python
r.Viennafold()
r.ViennaTargetEnergy('(((....)))')
```
