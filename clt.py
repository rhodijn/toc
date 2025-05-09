#!/usr/bin/env python3

# /// script
# requires-python= ">=3.12"
# dependencies = [
#     "typer",
# ]
# ///

import typer

def add(a: int, b: int):
    return a + b

if __name__ == '__main__':
    typer.run(add)