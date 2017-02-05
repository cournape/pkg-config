import string


def resolve_metadata(metadata, variables):
    resolved_metadata = {}

    for name, value in metadata.items():
        tpl = string.Template(value)
        resolved_metadata[name] = tpl.substitute(variables)

    return resolved_metadata


def resolve_variables(variables):
    old_variables = variables
    has_changed = True

    while has_changed:
        new_variables = {}
        for name, value in old_variables.items():
            tpl = string.Template(value)
            new_variables[name] = tpl.substitute(old_variables)

        for k in new_variables:
            if new_variables[k] != old_variables[k]:
                has_changed = True
                old_variables = new_variables
                break
        else:
            has_changed = False

    return new_variables
