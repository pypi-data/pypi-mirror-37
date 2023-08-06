from django.db.models import Model

from djangokarat.constraints import CheckKaratFields
from djangokarat.utils import (
    has_karat_fields, convert__all__to_fields, strip_square_brackets, prepare_data_to_karat,
    get_karat_id_fields, filter_relational_fields, switch_values_to_keys, send_data,
)

from django.db import models
models.options.DEFAULT_NAMES += ('karat_table', 'karat_fields')
models.options.Options.karat_fields = None
models.options.Options.karat_table = None

from . import Worker


class KaratModel(Model):
    # create delete call
    # check thru multiple tables same unique name
    # change how exclamation mark works

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
            model_data = prepare_data_to_karat(self)
            prepared_data = self._prepare_data(model_data)
            Worker.add(send_data, [prepared_data])

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        # if not has_karat_fields(self):
        #     return
        # unique_field = get_karat_id_fields(self)

    def _prepare_data(self, karat_fields_dict):
        karat_fields_dict['_table'] = self._meta.karat_table
        karat_fields_dict['_description'] = str(self)
        return karat_fields_dict
