import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


# This is part of CS50's distribution code for PSet8, Finance
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# modified to accommodate for negative values in html
def usd(value):
    """Format value as USD."""

    return f"${value:,.2f}".replace('$-', '-$')
