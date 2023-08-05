# `is_safe_url()`

Redirecting a visitor to another URL is common. It's also common that the 
redirect target is controllable by a visitor. One can often find a `?next` or
`?on_complete` GET parameter with the redirect target.

While this form of redirection is convenient, blindly redirecting a visitor to
the given target can easily lead to [Unvalidated Redirect and Forwards](https://www.owasp.org/index.php/Unvalidated_Redirects_and_Forwards_Cheat_Sheet).
Thus, one needs to check if the redirect target is "safe" before redirecting a
visitor.

The [Django web framework](https://djangoproject.com) has a utility function
`is_safe_url()` that attempts to validate a given target against a set of valid
hosts. This package unbundles the function and easily allows other projects to
use it.

```python
>>> from is_safe_url import is_safe_url
>>> is_safe_url("/redirect/target", {"example.com", "www.example.com"})
True
>>> is_safe_url("//example.com/redirect/target", {"example.com", "www.example.com"})
True
>>> is_safe_url("//evil.net/redirect/target", {"example.com"})
False
>>> is_safe_url("http://example.com/redirect/target", {"example.com"})
True
>>> is_safe_url("http://example.com/redirect/target", {"example.com"}, require_https=True)
False
>>> is_safe_url("https://example.com/redirect/target", {"example.com"}, require_https=True)
True
```

# Security

Please report security issues **privately** to the
[Django security team](security@djangoproject.com) or
[Markus Holtermann](info+security+is-safe-url@markusholtermann.eu).
