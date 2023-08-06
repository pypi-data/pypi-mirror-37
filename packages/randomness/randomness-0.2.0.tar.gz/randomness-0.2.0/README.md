Randomness Sources for Python
=============================


Current Features
----------------

* unified API to randomness sources
* API access to the system's true randomness generator
* a list of randomness providers to choose from
* provider flags which you can filter for


Planned Features
----------------

* comprehensive tests for randomness quality (dieharder, ENT, ...)
* more PRNGs (Wichmann-Hill, xorshift, ...)
* more TRNGs (VIA Padlock RNG, external hardware, ...)
* better API to filter and sort providers
* choice between wasteful and conserving usage of random bits,
  the latter most likely with a mixin
* adapter to provide the Numpy API for all randomness sources,
  most likely by way of a mixin


Usage
-----

You can instantiate a randomness source directly if you know it's there
(or if you handle the exception in case it's not):

```python3
from randomness import URandom

try:
    from randomness import Random

except ImportError:
    pass

random = URandom()
```

Or you can peruse the list of providers and select one out of those
(possibly filtering the list first):

```python3
from randomness import PROVIDERS, ProviderFlag

# filter randomness providers
my_providers = [provider for provider in PROVIDERS
                if provider.flags & ProviderFlag.NEVER_BLOCKING]

# dump provider names
for provider in my_providers:
    print(provider.name)

# instantiate a randomness context
chosen_provider = my_providers[0]
random = chosen_provider.cls()
```

From this point forward usage is the same as if you had done
`from random import Random; random = Random()`.

```python3
# perform a die roll
die_result = random.randint(1, 6)
print(die_result)

# select a random cheese
CHEESE_SHOP_PRODUCTS = ["Tilsit", "Cheddar", "Roquefort", "Gouda"]
cheese = random.choice(CHEESE_SHOP_PRODUCTS)
print(cheese)

# draw lottery numbers
amount_of_numbers = 49
amount_to_draw = 6
series = random.sample(range(1, amount_of_numbers + 1),
                       amount_to_draw)
print(series)
```
