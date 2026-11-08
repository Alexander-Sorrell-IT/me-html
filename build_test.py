#!/usr/bin/env python3
"""Rebuild test.html: embed the me-core script from me.html into the test template.

Usage:  python3 build_test.py     (run from the me/ folder)
Keeps me.html the single source of truth — test.html always tests the shipped core.
"""
import re, pathlib

here = pathlib.Path(__file__).parent
src = (here / "me.html").read_text()
core = re.search(r'<script id="me-core">.*?</script>', src, re.S).group(0)
head = (here / "_tpl_head.html").read_text().replace("<!--CORE-->", core)
tests = (here / "_tpl_tests.html").read_text()
(here / "test.html").write_text(head + tests)
print("test.html rebuilt:", len(head + tests), "bytes")
