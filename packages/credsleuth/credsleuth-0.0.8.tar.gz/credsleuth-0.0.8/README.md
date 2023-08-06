# Credential Sleuth
A rule driven library for detecting secrets and credentials within files and strings.

## Simple Usage
### Finding secrets in a string:
```python
import credsleuth

data = """
Hello, world
Password=123
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
Goodbye
"""
print(credsleuth.check_string(data))
```


### Finding secrets in a string:
```python
import credsleuth

print(credsleuth.check_string("filename.txt"))
```
## Advanced Usage
- Todo

## Installation
`pip install --user credsleuth`

## Writing Rules
See `rules.json` for an example to extent. 

## Todo
- Add some comments to codebase
- Add pretty output options for command line execution.
- Write a proper read me.