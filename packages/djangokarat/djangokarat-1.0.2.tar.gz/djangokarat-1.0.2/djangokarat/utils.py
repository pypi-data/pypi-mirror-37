def has_karat_fields(instance):
    if not instance._meta.karat_table and not instance._meta.karat_fields:
        return False
    return True


def convert__all__to_fields(instance):
    # Checks meta karat_fields for __all__ to add to fields
    if (instance._meta.karat_table and not instance._meta.karat_fields) or instance._meta.karat_fields == '__all__':
        instance._meta.karat_fields = [f.name for f in instance._meta.get_fields()]


def get_karat_id_fields(karat_fields):
    fields = []
    if isinstance(karat_fields, dict):
        for field in karat_fields.keys():
            if check_start_end_square_brackets(field):
                fields.append(karat_fields[field])

    else:
        for field in karat_fields:
            if check_start_end_square_brackets(field):
                fields.append(field)

    if not fields:
        raise AttributeError
    return fields


def filter_relational_fields(list):
    return [field for field in list if '__' in field]


def strip_exclamation_mark(field):
    if '!' not in field:
        return field
    field = field.replace('!', '')
    return field


def switch_values_to_keys(dict_to_swap):
    if not isinstance(dict_to_swap, dict):
        raise TypeError
    return dict((v, k) for k, v in dict_to_swap.items())


def check_start_end_square_brackets(field):
    if not field.startswith('[') or not field.endswith(']'):
        return False
    return True


def strip_square_brackets(field):
    if '[' not in field and ']' not in field:
        return field

    square_brackets = '[]'
    for bracket in square_brackets:
        field = field.replace(bracket, '')
    return field


def append_field_name_to_keys(dict_to_change, field_name):
    switched_dict = switch_values_to_keys(dict_to_change)
    for key, value in switched_dict.items():
        switched_dict[key] = "{}__{}".format(field_name, value)
    return switch_values_to_keys(switched_dict)
