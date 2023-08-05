# dappy

package to allow defining an API declaratively


## Example

```python
from dappy import API, Endpoint
ItunesAPI = API('itunes.apple.com', [
    Endpoint(
        'search', '/search',
        query_map={ 'search_string': 'term' }
    ),
    Endpoint('get', '/lookup', defaults={'id': '656270845'})
])
ItunesAPI.search(search_string='Hello, World')
ItunesAPI.get()
```

* Free software: MIT license
* Documentation: https://dappy.readthedocs.io.
