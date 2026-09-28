# lib/toml.py - minimaler TOML-Parser für CircuitPython
#
# Unterstützt einfache "schluessel = wert"-Zeilen mit Strings, Ganzzahlen,
# Kommazahlen und true/false sowie Kommentare (auch am Zeilenende).
# Nicht unterstützt: Tabellen/Sektionen ([abschnitt]) werden ignoriert,
# Listen, mehrzeilige Strings und Datumswerte.
#
# Achtung: dump()/dumps() schreibt nur "schluessel = wert"-Zeilen,
# Kommentare aus der Originaldatei gehen dabei verloren.


def _strip_comment(value):
    # Entfernt einen Kommentar (#) am Zeilenende, aber nicht innerhalb von Anführungszeichen
    quote = None
    for i, char in enumerate(value):
        if char in ('"', "'"):
            if quote is None:
                quote = char
            elif quote == char:
                quote = None
        elif char == "#" and quote is None:
            return value[:i].strip()
    return value.strip()


def _parse_value(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
        return value[1:-1]
    if value in ("true", "false"):
        return value == "true"
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def loads(s):
    data = {}
    for line in s.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("["):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = _parse_value(_strip_comment(value))
    return data


def load(f):
    return loads(f.read())


def dumps(data):
    out = []
    for k, v in data.items():
        if isinstance(v, bool):
            out.append(f"{k} = {'true' if v else 'false'}")
        elif isinstance(v, str):
            out.append(f'{k} = "{v}"')
        else:
            out.append(f"{k} = {v}")
    return "\n".join(out) + "\n"


def dump(data, f):
    f.write(dumps(data))
