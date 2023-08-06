import traceback
from threading import Thread
from multiprocessing import Queue

from djangokarat.utils import (
    prepare_relational_field_to_karat, prepare_data_to_karat, send_data, get_relation_model, get_self_related_name,
    filter_relational_fields, switch_values_to_keys, append_field_name_to_keys, merge_nested_dicts,
    strip_exclamation_mark, get_karat_id_fields, strip_square_brackets, get_relation_internal_type, update_fields_in_instance
)


class Worker(Thread):
    # allow mutliple idcolumns to retrieve 1 object
    # drop support for non-dict karat_fields
    queue = Queue()
    models = None

    def run(self):
        while True:
            method, args = self.queue.get()
            try:
                method(*args)
            except Exception:
                print(traceback.format_exc())

    @classmethod
    def add(cls, method, *args):
        cls.assign_karat_models()
        cls.queue.put((method, *args))

    @classmethod
    def add_sync(cls, data_array):
        cls.assign_karat_models()
        cls.add(cls.sync, [cls, data_array])

    @classmethod
    def assign_karat_models(cls):
        if cls.models:
            return
        # sets all models with karat attributes to local variable for later use
        from django.apps import apps
        models = apps.get_models()
        cls.models = list(((model._meta.original_attrs['karat_table'], model)
                           for model in models if 'karat_table' in model._meta.original_attrs))

    def sync(self, data_array):
        self.assign_karat_models()
        # all incoming data are parsed by their table names
        for data in data_array:
            for key in data.keys():
                used_tables = self.find_index_of_tables(self, key)
                self.add(self.update_or_create_instance, [self, used_tables, data[key]])

    def find_index_of_tables(self, table):
        # based on incoming data gets all indexes of models with `karat_table` where data will be saved
        tables_index = [index for index, model in enumerate(self.models) if model[0] == table]
        return tables_index

    def skip_empty_model(self, data, karat_fields):
        '''
        if there are multiple models in one table in karat, check if ours model has to be modified
        '''
        if isinstance(karat_fields, dict):
            should_skip = False
            id_columns = get_karat_id_fields(karat_fields)
            model_fields = switch_values_to_keys(karat_fields)
            for id_column in id_columns:
                # if there are data for field and field shouldn't be ignored
                if not str(data.get(id_column, '')).strip():
                    should_skip = True
        return should_skip

    def prepare_data_to_send(self, used_instances):
        ''' cycle to used instances and build them to single dictionary
        '''
        data_to_send = {}
        for instance in used_instances:
            data_to_send = {**prepare_data_to_karat(instance), **data_to_send}
            data_to_send['_table'] = instance._meta.karat_table
        return data_to_send

    def build_instance_map(self, model, fields, karat_fields, data):
        instance_map = {}
        for field in fields:
            parts = field.split('__')
            data_name = karat_fields[field]
            lookup_model_dict = self.build_relational_map_lookup(self, model, parts, data[data_name])
            instance_map = merge_nested_dicts(instance_map, lookup_model_dict)
        return instance_map

    def build_relational_map_lookup(self, model, parts, data_value):
        field_name = parts.pop(0)
        lookup_dictionary = {}
        if parts:
            field_model = get_relation_model(model, field_name)
            lookup_dictionary[field_name] = self.build_relational_map_lookup(self, field_model, parts, data_value)
            return lookup_dictionary
        else:
            return {field_name: data_value}

    def build_instance_from_map(self, model, instance_map):
        ''' gets instance based of input dictionary of values
        '''
        models_instance_map, models_instance_id_map = self.build_models_in_instance_map(self, model, instance_map)
        instance = self.get_or_create_instance_from_dict(self, model, models_instance_map)
        return instance, models_instance_id_map

    def update_instance_data_from_map(self, instance, instance_map, instance_id_dict):
        # print(instance, instance_map, instance_id_dict)
        updated_instance = self.update_or_create_instance_from_dict(self, instance, instance_map, instance_id_dict)
        return updated_instance

    def build_models_in_instance_map(self, model, instance_map, level=0):
        ''' recursively goes through built dictionary and each dict objects turns into id of object
        returns tuple.
        '''
        instance_id_only_map = {}
        has_dict = True
        while has_dict:
            # premise that dictionary hasn't dictionary
            has_dict = False
            # upfront check if in instance_map is any dictionary
            for instance_model_name, data in instance_map.items():
                if isinstance(data, dict):
                    has_dict = True

            for instance_model_name, data in instance_map.items():
                if isinstance(data, dict):
                    instance_model = get_relation_model(model, instance_model_name)
                    instance_model_relation_type = get_relation_internal_type(model, instance_model_name)
                    # recurse to get instance model instance
                    instance, instance_id_map = self.build_models_in_instance_map(
                        self, instance_model, data, level + 1)
                    instance_id = instance.pk
                    # after id is found, field name has to have `_id` appended
                    instance_model_name_with_id = "{}_id".format(instance_model_name)

                    instance_id_only_map[instance_model_name] = instance_id_map
                    # add and `_id` field name
                    if instance_model_relation_type == 'OneToOneField':
                        instance_map[instance_model_name] = instance
                    else:
                        instance_map[instance_model_name_with_id] = instance_id
                        # remove original name
                        instance_map.pop(instance_model_name)

                elif not has_dict and level > 0:
                    instance = self.get_or_create_instance_from_dict(self, model, instance_map)
                    instance_id_only_map['id'] = instance.id
                    return instance, instance_id_only_map
                else:
                    continue

        return instance_map, instance_id_only_map

    def get_or_create_instance_from_dict(self, model, data_dict):
        instance_model_filter = model.objects.filter(**data_dict)
        if instance_model_filter.exists():
            instance = instance_model_filter.get()
            return instance
        else:
            instance = model(**data_dict)
            if instance._meta.karat_fields:
                instance.save(_send=False)
            else:
                instance.save()
            return instance

    def update_or_create_instance_from_dict(self, instance, data_dict, instance_id_dict):
        for name, value in data_dict.items():
            if isinstance(value, dict):
                new_object = False
                inner_instance = getattr(instance, name, None)
                if name not in instance_id_dict or 'id' not in instance_id_dict[name]:
                    new_object = True
                inner_instance_model = get_relation_model(instance._meta.model, name)
                if not inner_instance and not new_object:
                    inner_instance = inner_instance_model.objects.get(id=instance_id_dict[name]['id'])

                if new_object:
                    inner_instance = self.get_or_create_instance_from_dict(self, inner_instance_model, value)
                    setattr(instance, name, inner_instance)
                else:
                    self.update_or_create_instance_from_dict(self, inner_instance, value, instance_id_dict[name])
            else:
                setattr(instance, name, value)
        if instance._meta.karat_fields:
            instance.save(_send=False)
        else:
            instance.save()
        return instance

    def update_or_create_instance(self, tables, data):
        used_instances = []
        # incoming data are sorted to their according tables by its unique id
        for table in tables:
            name, model = self.models[table]
            karat_fields = model._meta.karat_fields.copy()
            id_columns = get_karat_id_fields(karat_fields)
            # remove model id column so it cannot be changed in db
            check_model_fields = karat_fields.copy()
            # remove syncing column since it should be in every model (specified in constraints)
            for id_column in id_columns:
                check_model_fields.pop(id_column, None)

            # if model doesn't have fields to be updated skip it
            if self.skip_empty_model(self, data, check_model_fields):
                continue

            if isinstance(karat_fields, dict):
                # flip values for keys
                model_fields = switch_values_to_keys(karat_fields)
                # strip field_names of exclamation marks and brackets
                for field in model_fields.keys():
                    model_fields[field] = strip_exclamation_mark(model_fields[field])
                    model_fields[field] = strip_square_brackets(model_fields[field])
                # extract lookups from model
                lookup_fields = filter_relational_fields(model_fields.values())
                karat_fields = switch_values_to_keys(model_fields)
            else:
                model_fields = dict((field, field) for field in karat_fields)

            id_fields = [model_fields[id_column] for id_column in id_columns]
            data_fields = list(set(model_fields.values()) - set(id_fields))

            instance_relation_map = self.build_instance_map(self, model, id_fields, karat_fields, data)
            instance_data_map = self.build_instance_map(self, model, data_fields, karat_fields, data)

            instance, instance_id_dict = self.build_instance_from_map(self, model, instance_relation_map)
            updated_instance = self.update_instance_data_from_map(self, instance, instance_data_map, instance_id_dict)
            used_instances.append(updated_instance)

        # data_to_send = self.prepare_data_to_send(self, used_instances)
        # self.add(send_data, [data_to_send])

worker = Worker()
worker.daemon = True
worker.start()
name = "djangokarat"
