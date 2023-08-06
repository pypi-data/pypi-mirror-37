**rawgql** is a simple Python 3 framework for interacting with GraphQL endpoints.
There is very little to it; the GraphQL class simply accepts a raw query or
mutation passed as a string or file, packages it with the necessary headers
and optional query variables, and returns a python dictionary with the result.

There is little to no error checking, however there is a small pytest test
suite.

By default, the script will attempt to locate an `auth.json` file in a folder
named `gql/` in your project's working directory. Additionally, query files
can be stored in this folder and can be called from `GraphQL.query()` by
filename. `GraphQL.query()` also accepts passed strings. An optional argument
for query variables is available as well.

Check the function signatures and docstrings for more information. All of the
default folders and filenames can be changed with environmental variables or
by overriding after importing the module. 

