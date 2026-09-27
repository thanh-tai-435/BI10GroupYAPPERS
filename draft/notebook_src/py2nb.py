import json, re, sys
src, dst = sys.argv[1], sys.argv[2]
blocks = re.split(r"^# %%", open(src, encoding="utf-8").read(), flags=re.M)[1:]
cells = []
for b in blocks:
    head, _, body = b.partition("\n")
    body = body.strip("\n")
    if head.strip() == "[markdown]":
        text = "\n".join(re.sub(r"^# ?", "", l) for l in body.splitlines())
        cells.append({"cell_type": "markdown", "metadata": {}, "source": text})
    else:
        cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": body})
nb = {"cells": cells, "metadata": {"colab": {"provenance": []}, "kernelspec": {"name": "python3", "display_name": "Python 3"},
      "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 4}
json.dump(nb, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(cells), "cells ->", dst)
