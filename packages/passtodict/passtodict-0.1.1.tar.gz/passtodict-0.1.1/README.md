Decrypts [Password Store][1] passwords and creates a *dict*-like structure.

```sh
$ pass example.org
my-secret-password
login: JohnDoe
email: johndoe@example.org
```

```python
>>> import passtodict
>>> ex = passtodict('example.org')
>>> ex['login']
JohnDoe
>>> ex['email']
johndoe@example.org
>>> ex.PWD
my-secret-password
```

[1]: https://www.passwordstore.org/
