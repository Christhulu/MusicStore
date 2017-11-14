"""
    Run the Catalog web application.
"""

from catalog import app

app.secret_key = "super_secret_key"
app.debug = True
# start the web server with our app
app.run(host='0.0.0.0', port=5000)
