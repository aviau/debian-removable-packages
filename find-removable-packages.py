#!/usr/bin/env python3

from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool
import subprocess

def get_pkgs():
    with open("dqa.html", "r") as f:
        html = f.read()
    soup = BeautifulSoup(html, features="html.parser")
    a_tags = soup.find_all("a")

    pkgs = set()

    for tag in a_tags:
        href = tag.attrs.get("href", None)

        if not href or "/pkg/" not in href:
            continue

        pkg = href.split("/")[-1]

        pkgs.add(pkg)

    return list(pkgs)

def check_removable(pkg):
    output = subprocess.check_output(
        ["debian-rm", pkg],
    )

    removable = "No dependency problem found." in output.decode()

    return pkg, removable


def main():

    pkgs = get_pkgs()

    pool = ThreadPool(processes=16)

    for pkg, removable in pool.imap_unordered(check_removable, pkgs):
        if removable:
           print(f"{pkg} is removable")


if __name__ == "__main__":
    main()
