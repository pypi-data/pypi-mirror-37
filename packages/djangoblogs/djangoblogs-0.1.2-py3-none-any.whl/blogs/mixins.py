from django.core.exceptions import PermissionDenied
from .models import Author

class AuthorRequiredMixin:
    """
    Checks if the current user is an author
    """
    def dispatch(self, request, *args, **kwargs):
        try:
            author = Author.objects.get(user=request.user)
            if author.is_author:
                return super().dispatch(request, *args, **kwargs)
            else:
                raise PermissionDenied
        except Author.DoesNotExist: # pragma: no cover
            raise PermissionDenied        