import os
import re
from typing import Iterator, List, Optional

from flask import Flask, request
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def build_query(query, f) -> Iterator:
    res: Iterator
    query_items = query.split("|")
    res = map(lambda v: v.strip(), f)
    for item in query_items:
        if ":" in item:
            split_item = item.split(":")
            cmd = split_item[0]
            val = split_item[1]
        else:
            cmd = item
            val = ""
        res = apply_cmd(cmd, val, res)

    return res


def apply_cmd(cmd: str, val: str, list_in: Iterator) -> Iterator:
    if cmd == "filter":
        list_in = filter(lambda v, txt=val: txt in v, list_in)
    elif cmd == "regex":
        regex = re.compile(val)
        list_in = filter(lambda v: regex.search(v), list_in)
    elif cmd == "map":
        arg = int(val)
        list_in = map(lambda v, idx=arg: v.split(" ")[idx], list_in)
    elif cmd == "unique":
        list_in = iter(set(list_in))
    elif cmd == "sort":
        reverse = (val == "desc")
        list_in = iter(sorted(list_in, reverse=reverse))
    elif cmd == "limit":
        arg = int(val)
        list_in = iter(list(list_in)[:arg])

    return list_in


@app.route("/perform_query", methods=['POST'])  # Пример filter:GET|regex:images\/\w+\.jpg|sort:desc
def perform_query():
    try:
        query = request.form["query"]
        file_name = request.form["file_name"]
    except KeyError:
        raise BadRequest

    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        return BadRequest(description=f"{file_name} not found")

    with open(file_path) as f:
        res = build_query(query, f)
        content = "\n".join(res)

    return app.response_class(content, content_type="text/plain")


if __name__ == '__main__':
    app.run()
