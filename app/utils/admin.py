from django.contrib import admin
from django.utils.translation import gettext as _

other_info_fields = (
    (
        (
            _("Other Information"),
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )
    .__iter__()
    .__next__()
)
"""Default fields for created_at and updated_at in admin."""


def get_admin_context(request, extra_context=None):
    """Get default context dict for the admin site."""
    return {**admin.site.each_context(request), **(extra_context or {})}
