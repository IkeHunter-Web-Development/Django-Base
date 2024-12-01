import json

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter

from django.utils.safestring import mark_safe


from django.contrib import admin


class ModelAdminBase(admin.ModelAdmin):
    """Base class for all model admins."""

    prefetch_related_fields = []
    select_related_fields = []
    readonly_fields = ["created_at", "updated_at"]

    ###########################
    # Django method overrides #
    ###########################

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if len(self.prefetch_related_fields) > 0:
            return qs.prefetch_related(*self.prefetch_related_fields).select_related(*self.select_related_fields)
        else:
            return qs

    ########################
    # Custom admin methods #
    ########################

    def render_json(self, obj):
        """
        Convert obj to html json format.

        Reference: https://daniel.feldroy.com/posts/pretty-formatting-json-django-admin
        """

        if obj is None:
            return None
        print(obj)

        if isinstance(obj, dict) or isinstance(obj, list):
            obj = json.dumps(obj)

        response = json.dumps(json.loads(obj), indent=2)

        formatter = HtmlFormatter(style="colorful")

        response = highlight(response, JsonLexer(), formatter)
        response = response.replace("\\n", "<br>")
        style = "<style>" + formatter.get_style_defs() + "</style><br>"

        return mark_safe(style + response)
