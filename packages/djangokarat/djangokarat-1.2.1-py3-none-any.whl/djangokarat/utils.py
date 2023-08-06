import requests
import json

from django.conf import settings
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder

# TODO remove zfill in data send


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


def get_relation_model(model, field_name):
    # get model of relation field (FK, O2O) >= Django 2.0
    return model._meta.get_field(field_name).remote_field.model


def get_self_related_name(model, field_name):
    # get how attribute is named in referencing model
    return model._meta.get_field(field_name).remote_field.related_name


def get_relation_internal_type(model, field_name):
    # returns string value of relation (foreignkey, onetoonefield)
    return model._meta.get_field(field_name).get_internal_type()


def append_field_name_to_keys(dict_to_change, field_name):
    switched_dict = switch_values_to_keys(dict_to_change)
    for key, value in switched_dict.items():
        switched_dict[key] = "{}__{}".format(field_name, value)
    return switch_values_to_keys(switched_dict)


def update_fields_in_instance(instance, data_dict):
    for attribute, value in data_dict.items():
        setattr(instance, attribute, value)
    instance.save()
    return instance


def prepare_relational_field_to_karat(instance, field):
    ''' get data of instance at the end of relational field  
    '''
    fields = field.split('__')
    field_data = instance
    for field in fields:
        if field == 'id':
            field_data = getattr(field_data, field, None)
            field_data = str(field_data).zfill(8)
        else:
            field_data = getattr(field_data, field, None)
    return field_data


def merge_nested_dicts(base_dict, merging_dict, path=None):
    ''' immutates base dict and extends it with merging dict
    '''
    if path is None:
        path = []
    for key in merging_dict:
        if key in base_dict:
            if isinstance(base_dict[key], dict) and isinstance(merging_dict[key], dict):
                merge_nested_dicts(base_dict[key],  merging_dict[key], path + [str(key)])
            elif base_dict[key] == merging_dict[key]:
                pass  # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            base_dict[key] = merging_dict[key]
    return base_dict


def prepare_data_to_karat(instance):
    switched_karat_fields = switch_values_to_keys(instance._meta.karat_fields)
    cleaned_karat_fields = switched_karat_fields.copy()
    # clean fields of controlling tokens
    for name, value in switched_karat_fields.items():
        cleaned_karat_fields[name] = strip_square_brackets(cleaned_karat_fields[name])
        if '!' in value:
            cleaned_karat_fields.pop(name)
    switched_karat_fields = cleaned_karat_fields
    # have dictionary ready to get karat field names
    karat_fields = switch_values_to_keys(switched_karat_fields)
    # gets all flat data (non-relational)
    model_data = model_to_dict(instance, fields=switched_karat_fields.values())
    # build dictionary with keys from karat db and with flat data
    karat_data = {name: model_data[value] for name, value in switched_karat_fields.items() if value in model_data}
    relational_fields = filter_relational_fields(switched_karat_fields.values())
    # get data of relational fields
    for relation_field in relational_fields:
        field = relation_field.split('__')[0]
        new_model = getattr(instance, field)
        field_name = karat_fields[relation_field]
        if not new_model:
            continue
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
