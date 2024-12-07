def clever_function():
    return u'HELLO'

app.jinja_env.globals.update(clever_function=clever_function)