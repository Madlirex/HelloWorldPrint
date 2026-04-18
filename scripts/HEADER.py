HEADER = """import builtins

RENAMES = {
    "vytlač": "print",
    "vtlač": "input",
    "dĺžka": "len",
    "rozsah": "range"
}

def _make_blocked(old_name, new_name):
    def blocked(*args, **kwargs):
        raise RuntimeError(f"Use '{new_name}' instead of '{old_name}'")
    return blocked

for new_name, old_name in RENAMES.items():
    original = getattr(builtins, old_name)

    globals()[new_name] = original

    globals()[old_name] = _make_blocked(old_name, new_name)\n\n"""