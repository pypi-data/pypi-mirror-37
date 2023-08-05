Enigma Public SDK
=================

The Enigma SDK helps developers build Python applications that integrate with Enigma Public. The SDK is available as a Python package you can install using pip:

    $ pip install enigma-sdk

The Python SDK simplifies app development in several important ways versus using the Enigma Public API directly via calls to HTTP endpoints:

- The SDK handles all HTTP requests for you. This includes automatic retries, connection pooling, and passing of API keys.
- It generates iterators automatically if pagination is required, and supports Python list slicing for easy access to resources.
- It provides a set of “convenience” methods to implement common tasks that would otherwise require multiple API calls.
- It returns responses as Python objects you can query using familiar object.attribute patterns, rather than navigating JSON hierarchies.
