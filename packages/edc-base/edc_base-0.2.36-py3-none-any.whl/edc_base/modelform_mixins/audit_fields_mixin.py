from ..utils import get_utcnow


class AuditFieldsMixin:

    """Updates audit fields with username /datetime on create and
    modify.
    """

    def update_system_fields(self, request, instance, change):
        if not change:
            instance.user_created = request.user.username
            instance.created = get_utcnow()
        instance.user_modified = request.user.username
        instance.date_modified = get_utcnow()
        return instance

    def form_valid(self, form):
        form.instance = self.update_system_fields(
            self.request, form.instance, change=True)
        return super(AuditFieldsMixin, self).form_valid(form)
