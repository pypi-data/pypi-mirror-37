from django.contrib.admin.utils import flatten_fieldsets
from django.urls import reverse
from django.utils.html import format_html
from django.utils.inspect import get_func_args

from .helpers import get_attribute, has_attribute
from .models.helpers import is_editable


class ChangeUrl:
    def __init__(self, field, description=None):
        self.field = field
        self.short_description = description or field

    def __call__(self, obj):
        try:
            obj = get_attribute(obj, self.field)
        except AttributeError:
            return '-'

        url = object_admin_rel_url(obj)
        return format_html('<a href="{}">{}</a>', url, obj)


def object_admin_rel_url(obj):
    return reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=(obj.pk,))


def foreign_field(field_name, short_description=None, admin_order_field=None, boolean=False):
    assert '__' not in field_name, 'use . as delimiter for traversing relations'

    def accessor(obj):
        if not has_attribute(obj, field_name):
            return None
        attribute = get_attribute(obj, field_name)
        if callable(attribute):
            return attribute()
        return attribute

    # Set attribute so we can get is outside
    accessor.attribute = field_name
    short_description = short_description or field_name.replace('.', ' ').replace('_', ' ')
    short_description = short_description.capitalize()
    accessor.short_description = short_description
    accessor.admin_order_field = admin_order_field
    accessor.boolean = boolean
    return accessor


class ReadOnlyFieldsAdminMixin:
    editable_fields = []
    exclude = []

    def get_readonly_fields(self, request, obj=None):
        args = get_func_args(self.has_add_permission)
        if 'obj' in args:
            has_add_permission = self.has_add_permission(request, obj)
        else:
            has_add_permission = self.has_add_permission(request)

        if obj is None and has_add_permission:
            return super().get_readonly_fields(request, obj)

        if self.fields or self.fieldsets:
            fields = flatten_fieldsets(self.get_fieldsets(request, obj))
        else:
            fields = [
                field.name for field in self.model._meta.fields
                if is_editable(field)
            ]

        exclude = self.get_exclude(request, obj)
        editable_fields = self.get_editable_fields(request, obj)
        return [
            field for field in fields
            if field not in editable_fields and field not in exclude
        ]

    def get_editable_fields(self, request, obj=None):
        return self.editable_fields


class NoAddDeleteAdminMixin:
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ReadOnlyAdminMixin(ReadOnlyFieldsAdminMixin, NoAddDeleteAdminMixin):
    def has_change_permission(self, request, obj=None):
        if hasattr(self, 'has_view_permission'):  # Django >= 2.1
            return False
        return super().has_change_permission(request, obj=obj)
