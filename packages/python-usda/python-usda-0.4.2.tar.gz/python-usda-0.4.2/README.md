# python-usda

python-usda is a fork of [pygov](https://pypi.org/project/pygov/) focused on [USDA's Food Composition Database API](http://ndb.nal.usda.gov/ndb/doc/). Browse full documentation on [Read the Docs](https://python-usda.readthedocs.io/en/latest)

## Installation

```
pip install python-usda
```

## Usage

``` python
from usda.client import UsdaClient

client = UsdaClient("YOUR_API_KEY")
foods = client.list_foods(5)

for food in foods:
    print(food.name)
```

Result:

```
Abiyuch, raw
Acerola juice, raw
Acerola, (west indian cherry), raw
Acorn stew (Apache)
Agave, cooked (Southwest)
```
