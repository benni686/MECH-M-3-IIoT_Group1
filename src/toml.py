# lib/toml.py - minimal TOML parser for CircuitPython
def loads(s):
    data = {}
    for line in s.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"')
        if value.isdigit():
            value = int(value)
        elif value.lower() in ("true", "false"):
            value = value.lower() == "true"
        data[key] = value
    return data

def load(f):
    return loads(f.read())

def dumps(data):
    out = []
    for k, v in data.items():
        if isinstance(v, str):
            out.append(f'{k} = "{v}"')
        else:
            out.append(f"{k} = {v}")
    return "\n".join(out)

def dump(data, f):
    f.write(dumps(data))
