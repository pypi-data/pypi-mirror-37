from django.db import models


class CamelCaseOneToOneField(models.OneToOneField):
    def __init__(self, to, on_delete, to_field=None, **kwargs):
        attr_name = kwargs.pop('attr_name', None)
        super().__init__(to, on_delete, to_field=to_field, **kwargs)
        self.attr_name = attr_name

    def get_attname(self):
        return self.attr_name or super().get_attname()


class CamelCaseForeignKey(models.ForeignKey):
    def __init__(self, to, on_delete, related_name=None,  # pylint: disable=too-many-arguments
                 related_query_name=None, limit_choices_to=None, parent_link=False, to_field=None,
                 db_constraint=True, **kwargs):
        attr_name = kwargs.pop('attr_name', None)
        super().__init__(to, on_delete, related_name, related_query_name, limit_choices_to,
                         parent_link, to_field, db_constraint, **kwargs)
        self.attr_name = attr_name

    def get_attname(self):
        return self.attr_name or super().get_attname()

