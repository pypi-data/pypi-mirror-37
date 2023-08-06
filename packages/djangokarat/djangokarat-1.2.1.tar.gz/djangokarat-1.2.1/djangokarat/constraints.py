from django.db.models.sql.query import Query
from django.core import checks
from djangokarat.utils import (filter_relational_fields, switch_values_to_keys, strip_square_brackets,
                               strip_exclamation_mark, check_start_end_square_brackets)


class CheckKaratFields:

    def __init__(self, cls):
        self.cls = cls
        self.karat_table = cls._meta.karat_table
        self.karat_fields = cls._meta.karat_fields
        self.model_fields = cls._meta.get_fields()
        self.model_fields_names = [field.name for field in self.model_fields]
        self.is_dict = isinstance(self.karat_fields, dict)

    def is_relation(self, field):
        if '__' in field:
            return True
        return False

    def extract_field_name_from_lookups(self, field_array=None):
        ''' gets all fields with `__`. Extracts first part of name and replaces 
        lookup with only field name
        '''
        if not field_array:
            if self.is_dict:
                field_array = self.karat_fields.keys()
            else:
                field_array = self.karat_fields
        field_lookups = [field for field in field_array if '__' in field]
        field_array = list(set(field_array) - set(field_lookups))
        lookups_first_part = []
        for lookup in field_lookups:
            if check_start_end_square_brackets(lookup):
                stripped_lookup = strip_square_brackets(lookup)
                lookups_first_part.append('[{}]'.format(stripped_lookup.split('__')[0]))
            else:
                lookups_first_part.append(lookup.split('__')[0])

        return field_array + lookups_first_part

    def strip_miscellaneous_chars_from_fields(self, strip_function):
        ''' remove all unwanted characters from karat_fields to work with only field 
        names without i.e. `!`
        '''
        if self.is_dict:
            switched_karat_fields = switch_values_to_keys(self.karat_fields)
            for key in switched_karat_fields.keys():
                switched_karat_fields[key] = strip_function(switched_karat_fields[key])
            self.karat_fields = switch_values_to_keys(switched_karat_fields)
        else:
            for index, field in enumerate(self.karat_fields):
                self.karat_fields[index] = strip_function(field)

    def check_karat_table(self):
        errors = []
        if not self.karat_table and self.karat_fields:
            errors.append(
                checks.Error(
                    'missing field `karat_table` in Meta',
                    hint="add field `karat_table` to Meta or remove field `karat_fields`",
                    obj=self.cls,
                    id='karat.E001'
                )
            )
        elif not isinstance(self.karat_table, str):
            errors.append(
                checks.Error(
                    'field `karat_table` must be string',
                    obj=self.cls,
                    id='karat.E002'
                )
            )
        if self.karat_table and not self.karat_fields:
            errors.append(
                checks.Warning(
                    'missing field `karat_fields` in Meta',
                    hint="if not added all fields be used to karat_fields similiar to `__all__`",
                    obj=self.cls,
                    id='karat.W001'
                )
            )
        return errors

    def check_karat_fields(self):
        errors = []
        if (
            (isinstance(self.karat_fields, str) and self.karat_fields != '__all__')
            or not isinstance(self.karat_fields, (str, dict, list))
        ):
            errors.append(
                checks.Error(
                    'field `karat_fields` has to be `__all__`, list or dict',
                    hint="change field to correct type",
                    obj=self.cls,
                    id='karat.E003'
                )
            )
        if self.karat_fields and not '__all__':
            for field in self.karat_fields:
                if not field in self.model_fields_names:
                    errors.append(
                        checks.Error(
                            "doesn't have field {}".format(field),
                            hint="Correct typo in model",
                            obj=self.cls,
                            id='karat.E004'
                        )
                    )
        elif self.is_dict:
            karat_fields = self.extract_field_name_from_lookups(self.karat_fields.keys())
            for field in karat_fields:
                stripped_field = strip_square_brackets(field)
                if stripped_field not in self.model_fields_names:
                    errors.append(
                        checks.Error(
                            "doesn't have field {}".format(field),
                            hint="Correct typo in model key",
                            obj=self.cls,
                            id='karat.E004'
                        )
                    )

        return errors

    def check_uniqueness(self):
        errors = []
        unique = False

        if self.is_dict:
            karat_fields_keys = self.karat_fields.keys()
            karat_fields = self.extract_field_name_from_lookups(karat_fields_keys)
        else:
            karat_fields = self.karat_fields

        for field in karat_fields:
            if check_start_end_square_brackets(field):
                unique = True
                stripped_field = strip_square_brackets(field)
                model_field = self.cls._meta.get_field(stripped_field)
                model_field_internal_type = model_field.get_internal_type()
                if model_field_internal_type != 'OneToOneField' and model_field_internal_type != 'ForeignKey' and not model_field.unique:
                    errors.append(
                        checks.Warning(
                            "field is used as pk for connecting databases, but isn't unique",
                            hint="change {} to unique".format(field),
                            obj=self.cls,
                            id='karat.W002'
                        )
                    )

        if not unique:
            errors.append(
                checks.Error(
                    "class doesn't have unique in `karat_fields` used to connect dbs",
                    hint="Add unique field for id from karat db",
                    obj=self.cls,
                    id='karat.E005'
                )
            )
        self.strip_miscellaneous_chars_from_fields(strip_square_brackets)
        return errors

    def check_lookups(self):
        if self.is_dict:
            relational_fields = filter_relational_fields(self.karat_fields.keys())
        else:
            relational_fields = filter_relational_fields(self.karat_fields)

        errors = []
        if not relational_fields:
            return errors

        query = Query(self.cls)
        for field in relational_fields:
            lookups, parts, _ = query.solve_lookup_type(field)
            if lookups:
                errors.append(
                    checks.Error(
                        "There can't be lookups or not existing fields in relation",
                        hint="Fix {} to point to model field".format(field),
                        obj=self.cls,
                        id='karat.E006'
                    )
                )
        return errors

    def check_exclamation_error(self, field):
        if not field.startswith('!') and '!' in field:
            return checks.Error(
                "Exclamation mark must be at the beginning of field",
                hint="Remove or move exclamation mark in {}".format(field),
                obj=self.cls,
                id='karat.E007'
            )

    def check_exclamation_fields(self):
        errors = []

        if self.is_dict:
            for key in self.karat_fields.keys():
                if '!' not in key:
                    continue
                error = self.check_exclamation_error(key)
                if error:
                    errors.append(error)
        else:
            for field in self.karat_fields:
                if '!' not in field:
                    continue
                error = self.check_exclamation_error(field)
                if error:
                    errors.append(error)
        self.strip_miscellaneous_chars_from_fields(strip_exclamation_mark)
        return errors
