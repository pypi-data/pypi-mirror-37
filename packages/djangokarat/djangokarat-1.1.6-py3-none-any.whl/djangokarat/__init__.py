import traceback
from threading import Thread
from multiprocessing import Queue

from djangokarat.utils import (
    prepare_relational_field_to_karat, prepare_data_to_karat, send_data,
    filter_relational_fields, switch_values_to_keys, append_field_name_to_keys,
    strip_exclamation_mark, get_karat_id_fields, strip_square_brackets
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
                if '!' not in model_fields[id_column] and not str(data.get(id_column, '')).strip():
                    should_skip = True
        return should_skip

    def get_relation_model(self, model, field_name):
        # get model of relation field (FK, O2O) >= Django 2.0
        return model._meta.get_field(field_name).remote_field.model

    def get_self_related_name(self, model, field_name):
        # get how attribute is named in referencing model
        return model._meta.get_field(field_name).remote_field.related_name

    def get_lookup_relation(self, model, parts, value, unique_fields_dict):
        part = parts.pop(0)
        part_model = self.get_relation_model(self, model, part)
        # what type of relational connection it is (1:N, 1:1, M:N)
        relation_model_field_type = model._meta.get_field(part).get_internal_type()
        check_fields_dict = {}
        object_exists = True
        # 1:1 has check to ensure that if one part doesn't exists it gets created
        if relation_model_field_type == 'OneToOneField':
            field_related_name = self.get_self_related_name(self, model, part)
            # prepare query lookup for related model
            check_fields_dict = append_field_name_to_keys(unique_fields_dict, field_related_name)
            # model exists and has/hasn't relation with current model
            object_exists = part_model.objects.filter(**check_fields_dict).exists()
        instance = self.get_main_id_model_relation(self, part_model, parts, value, object_exists, check_fields_dict)
        return instance

    def get_main_id_model_relation(self, model, parts, value, object_exists=True, unique_fields_dict={}):
        ''' gets or creates relational models filled with data
        '''
        part = parts.pop(0)
        if parts:
            relation_model = self.get_relation_model(self, model, part)
            # recursively traverse to the end of lookup while preparing model instancees
            instance = self.get_main_id_model_relation(self, relation_model, parts, value)
            # filters top most model instance for given lookup
            model_filter = model.objects.filter(**{part: instance.pk}, **unique_fields_dict)
            if object_exists and model_filter.exists():
                relation_model_instance = model_filter.get()
            else:
                relation_model_instance = model(**{part: instance})
                relation_model_instance.save(_send=False)

            return relation_model_instance
        else:
            instance, _ = model.objects.get_or_create(**{part: value})
            return instance

    def build_instance_attributes_dictionary(self, data, id_columns, model_fields):
        ''' prepare data for model instance. Sort out immediate data for model and prepare relational models
        '''
        instance_dict = {}
        instance_check_dict = {}
        for id_column in id_columns:
            field = model_fields[id_column]
            if '__' not in field:
                # copy data to both dictionaries
                id_columns.remove(id_column)
                instance_dict[field] = data[id_column]
            instance_check_dict[field] = data[id_column]

        return instance_dict, instance_check_dict

    def build_instance_relation_models(self, model, parts, value):
        '''
        recursively traverse through each relational field in model until field value can be saved.
        Then save each instance of model so there is not conflict due to unsaved models when passed back to instance
        '''
        part = parts.pop(0)
        if parts:

            relation_model_instance = getattr(model, part)
            if not relation_model_instance:
                # create instance of model
                relation_model = self.get_relation_model(self, model, part)
                relation_model_instance = relation_model()

            # since it is relational field again call recurse
            setattr(
                relation_model_instance,
                part,
                self.build_instance_relation_models(self, relation_model_instance, parts, value)
            )
            relation_model_instance.save(_send=False)
            return relation_model_instance
        else:
            # End of chain of relational fields. Save value to field and wrap back
            setattr(model, part, value)
            return model

    def prepare_data_to_send(self, used_instances):
        ''' cycle to used instances and build them to single dictionary
        '''
        data_to_send = {}
        for instance in used_instances:
            data_to_send = {**prepare_data_to_karat(instance), **data_to_send}
        return data_to_send

    def update_or_create_instance(self, tables, data):
        used_instances = []
        # incoming data are sorted to their according tables by its unique id
        for table in tables:
            name, model = self.models[table]
            karat_fields = model._meta.karat_fields.copy()
            id_columns = get_karat_id_fields(karat_fields)
            # remove model id column so it cannot be changed in db
            karat_fields.pop('id', None)
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

            lookup_fields_dict = {}
            # remove lookup fields from data, because these data can't be used in setattr of instance
            for lookup in lookup_fields:
                lookup = strip_square_brackets(lookup)
                karat_field_name = karat_fields[lookup]
                if karat_field_name not in id_columns:
                    lookup_fields_dict[lookup] = data[karat_field_name]

            # hotfix - TODO: has one traverse
            try:
                # prepare data to retrieve or create instance by incoming data.
                # Check dict has object pks instead of object reference
                instance_dict, instance_check_dict = self.build_instance_attributes_dictionary(
                    self, data, id_columns, model_fields)
                # unique id from incoming data are retrieved or created in local db
                for id_column in id_columns:
                    parts = model_fields[id_column].split('__')
                    # get field name for field in model
                    field_name = parts[0]
                    same_models = [field for field in model_fields.keys() if field_name in field and '__' in field]
                    instance = self.get_lookup_relation(self, model, parts, data[id_column], instance_check_dict)
                    # save instance and its pk to separate dictionaries
                    instance_dict[field_name] = instance
                    instance_check_dict[field_name] = instance.pk
                    lookup_fields.remove(model_fields[id_column])
            except Exception:
                continue

            model_filter = model.objects.filter(**instance_dict)
            if model_filter.exists():
                instance = model_filter.get()
            else:
                instance = model.objects.create(**instance_dict)

            # get all fields which are defined in `karat_fields` in model and prepare data to be updated
            model_data = {model_fields[key]: value for key, value in data.items() if key in model_fields}
            # updates data of instance
            for attr, value in model_data.items():
                setattr(instance, attr, value)

            if lookup_fields_dict:
                for field in lookup_fields:
                    parts = field.split('__')
                    # name of relational field in model
                    instance_field_name = parts[0]
                    built_relation_instance = self.build_instance_relation_models(
                        self,
                        instance,
                        parts,
                        lookup_fields_dict[field]
                    )
                    setattr(instance, instance_field_name, built_relation_instance)
            instance.save(_send=False)
            used_instances.append(instance)

        data_to_send = self.prepare_data_to_send(self, used_instances)
        self.add(send_data, [data_to_send])

worker = Worker()
worker.daemon = True
worker.start()
name = "djangokarat"
