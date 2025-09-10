# user = {
#     "name": "Alice",
#     "age": 30,
#     "active": True
# }

# for key, value in user.items():
#     print(key, value)

# from .name import NAME

# def greet(name: str) -> str:
#     return f"Hello, {name}!"

# import ast
# from pathlib import Path

# here = Path(__file__).parent
# with open(here / "greet.pyexp") as f:
#     expr = f.read()

# greet = ast.literal_eval(expr)

# print(greet(NAME))

from .tree import siteTree as posts
from .templates.postFragment import postFragment

for key, value in posts.items():
    print(postFragment(value, key))