# Discord App Manager
![Built With Love :)](https://forthebadge.com/images/badges/built-with-love.svg)
![Made with Python](https://forthebadge.com/images/badges/made-with-python.svg)

![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
[![PyPi](https://img.shields.io/v/dam.svg)](https://pypi.org/pypi/dam/)

A simple package for uploading and deleting Discord Rich Presence images.

### Example
```python3
from dam import login

session = login(email=EMAIL, password=PASSWORD)
app = session.get_app(name="Listening to Music :)")
image_id = app.upload_image('path/to/image.png')
app.delete_image(image_id)
```
