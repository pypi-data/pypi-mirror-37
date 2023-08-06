import csv
from warnings import warn
from .exceptions import TransformationError

def delim_reader(input, transformations, *args, **kwargs):
    on_error = kwargs.pop('on_error', None)
    rules = _load_rules(transformations)
    reader = csv.DictReader(input, *args, **kwargs)
    row_num = 1

    for row in reader:
        row_num += 1
        try:
            yield _transform_dict(row, rules)
        except Exception as err:
            new_error = TransformationError(
                "%s: %s, in line %d" % (err.__class__.__name__, err, row_num),
                record=row
            )
            if on_error:
                on_error(new_error)
            else:
                raise new_error


def _load_rules(transformations):
    rules = []
    for rule in transformations:
        if "to" in rule:
            rules.append(rule)
        else:
            warn("Missing 'to' field in rule %s" % rule)
    return rules


def _transform_dict(input_row, rules):
    row = {}
    for rule in rules:
        via = rule.get("via", lambda x:x)
        if "from" in rule:
            value = via(input_row[rule["from"]])
        else:
            value = via(row)
        _update_dict(row, rule["to"], value)
    return row


def _update_dict(dictionary, key, value):
    keys = key.split('.')
    head = keys[0:-1]
    tail = keys[-1]
    for h in head:
        if h not in dictionary:
            dictionary[h] = {}
        dictionary = dictionary[h]
    dictionary[tail] = value
