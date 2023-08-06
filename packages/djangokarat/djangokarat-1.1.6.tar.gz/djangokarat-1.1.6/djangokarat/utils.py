import requests
import json

from django.conf import settings
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder


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


def prepare_relational_field_to_karat(instance, field):
    ''' get data of instance at the end of relational field  
    '''
    fields = field.split('__')
    field_data = instance
    for field in fields:
        field_data = getattr(field_data, field)
    return field_data


def prepare_data_to_karat(instance):
    karats = switch_values_to_keys(instance._meta.karat_fields)
    # clean fields of controlling tokens
    for name, value in karats.items():
        karats[name] = strip_square_brackets(karats[name])
        if '!' in value:
            karats.pop(name)
    # have dictionary ready to get karat field names
    karat_fields = switch_values_to_keys(karats)
    # gets all flat data (non-relational)
    model_data = model_to_dict(instance, fields=karats.values())
    # build dictionary with keys from karat db and with flat data
    karat_data = {name: model_data[value] for name, value in karats.items() if value in model_data}
    relational_fields = filter_relational_fields(karats.values())
    # get data of relational fields
    for relation_field in relational_fields:
        field = relation_field.split('__')[0]
        new_model = getattr(instance, field)
        field_name = karat_fields[relation_field]
        if new_model._meta.karat_table == instance._meta.karat_table:
            karat_data = {**prepare_data_to_karat(new_model), **karat_data}
        else:
            karat_data[field_name] = prepare_relational_field_to_karat(instance, relation_field)
    return karat_data


def send_data(data):
    print(data)
    if hasattr(settings, 'AGENT_URL'):
        r = requests.post('{}/accept-data/'.format(settings.AGENT_URL),
                          data=json.dumps(data, cls=DjangoJSONEncoder))
