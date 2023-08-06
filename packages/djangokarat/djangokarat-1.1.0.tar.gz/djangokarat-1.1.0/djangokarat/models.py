import requests
import json

from django.conf import settings
from django.db.models import Model
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder

from djangokarat.constraints import CheckKaratFields
from djangokarat.utils import (has_karat_fields, convert__all__to_fields, strip_square_brackets,
                               get_karat_id_fields, filter_relational_fields, switch_values_to_keys)

from . import Worker

from django.db import models
models.options.DEFAULT_NAMES += ('karat_table', 'karat_fields')
models.options.Options.karat_fields = None
models.options.Options.karat_table = None


class KaratModel(Model):
    # resolve why you have to put model to array when registering to admin
    # create delete call
    # delete in multiple tables
    # check thru multiple tables same unique name

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        convert__all__to_fields(self)

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        convert__all__to_fields(cls)
        errors.extend(cls._check_karat_meta(**kwargs))
        return errors

    @classmethod
    def _check_karat_meta(cls, **kwargs):
        errors = []
        # if karat params aren't there, don't check errors for them
        if not has_karat_fields(cls):
            return errors

        karat_check = CheckKaratFields(cls)
        # upfront model checks
        errors.extend(karat_check.check_karat_table())
        errors.extend(karat_check.check_exclamation_fields())
        errors.extend(karat_check.check_karat_fields())
        errors.extend(karat_check.check_uniqueness())
        errors.extend(karat_check.check_lookups())
        return errors

    def save(self, _send=True, *args, **kwargs):
        super().save(*args, **kwargs)
        if not has_karat_fields(self):
            return
        if _send:
            prepared_karat_fields = self._prepare_karat_fields()
            prepared_data = self._prepare_data(prepared_karat_fields)
            print(prepared_data)
            self._send_data(prepared_data)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        # if not has_karat_fields(self):
        #     return
        # unique_field = get_karat_id_fields(self)

    def _prepare_karat_fields(self):
        if isinstance(self._meta.karat_fields, dict):
            switched_fields = switch_values_to_keys(self._meta.karat_fields)
            stripped_switched_fields = {key: strip_square_brackets(value) for key, value in switched_fields.items()}
            karat_fields = switch_values_to_keys(stripped_switched_fields)
            extracted_dict = model_to_dict(self, fields=karat_fields.keys())
            # rename fields to match karat fields
            prepared_karat_fields = {karat_fields[k]: v for k, v in extracted_dict.items()}

            lookup_fields = filter_relational_fields(karat_fields.keys())
            # lookup related model fields and search for their data. Then append to rest
            for field in lookup_fields:
                # django method for splitting up lookups and field names
                parts = field.split('__')
                lookup_data = self._get_relation_data(parts, self)
                karat_name = karat_fields[field]
                prepared_karat_fields[karat_name] = lookup_data

        else:
            prepared_karat_fields = model_to_dict(self, fields=self._meta.karat_fields)
        return prepared_karat_fields

    def _get_relation_data(self, parts, model):
        if not model:
            return None
        field = parts.pop(0)
        if not parts:
            # gets data from instance by string
            return getattr(model, field)
        else:
            next_model = getattr(model, field)
            return self._get_relation_data(parts, next_model)

    def _prepare_data(self, karat_fields_dict):
        karat_fields_dict['_table'] = self._meta.karat_table
        karat_fields_dict['_description'] = str(self)
        return karat_fields_dict

    def _send_data(self, data):
        if hasattr(settings, 'AGENT_URL'):
            r = requests.post('{}/accept-data/'.format(settings.AGENT_URL),
                              data=json.dumps(data, cls=DjangoJSONEncoder))
