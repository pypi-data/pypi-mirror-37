# coding=utf-8
"""
permission_required decorator for generic classbased view from django 1.3
"""
from functools import wraps
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.utils.decorators import available_attrs
from django.views.generic import ListView, DetailView
from django.views.generic.detail import BaseDetailView, SingleObjectMixin
from django.views.generic.list import BaseListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, BaseCreateView, BaseUpdateView, BaseDeleteView
from simple_permissions.decorators.utils import redirect_to_login


def permission_required(perm=None, queryset=None,
                        login_url=None, raise_exception=False):
    """
    Permission check decorator for classbased generic view

    This decorator works as class decorator
    DO NOT use ``method_decorator`` or whatever while this decorator will use
    ``self`` argument for method of classbased generic view.

    Parameters
    ----------
    perm : string
        A permission string
    queryset_or_model : queryset or model
        A queryset or model for finding object.
        With classbased generic view, ``None`` for using view default queryset.
        When the view does not define ``get_queryset``, ``queryset``,
        ``get_object``, or ``object`` then ``obj=None`` is used to check
        permission.
        With functional generic view, ``None`` for using passed queryset.
        When non queryset was passed then ``obj=None`` is used to check
        permission.

    Examples
    --------
    >>> @permission_required('write')
    >>> class UpdateAuthUserView(UpdateView):
    ...     pass
    """

    def wrapper(cls):
        def dispatch_wrapper(view_func):
            @wraps(view_func, assigned=available_attrs(view_func))
            def inner(self, user, *args, **kwargs):
                has_perm = True

                if not hasattr(user, 'is_authenticated'):
                    user_obj = user.user

                try:
                    obj = get_object_from_classbased_instance(self, queryset, user, *args, **kwargs)
                except Exception as e:
                    # if an error occured for authenticated users leave the application
                    # normal handling
                    if user_obj.is_authenticated:
                        raise e

                    # otherwise require login or PermissionDenied exception (this information is private)
                    has_perm = False
                    obj = None

                model = type(obj)
                if hasattr(model, '_permission_logics'):
                    permission = perm
                    if permission is None:
                        if issubclass(cls, CreateView) | issubclass(cls, UpdateView) | issubclass(cls, DeleteView):
                            permission = 'write'
                        elif issubclass(cls, DetailView) | issubclass(cls, ListView):
                            permission = 'read'
                        elif issubclass(cls, BaseCreateView) | issubclass(cls, BaseUpdateView) | issubclass(cls, BaseDeleteView):
                            permission = 'write'
                        elif issubclass(cls, BaseDetailView) | issubclass(cls, BaseListView):
                            permission = 'read'
                        else:
                            return PermissionDenied
                    has_perm = all([logics.has_perm(user_obj, permission, obj=obj) for logics in model._permission_logics])

                if not has_perm:
                    if raise_exception:
                        raise PermissionDenied
                    else:
                        return redirect_to_login(user, login_url)
                return view_func(self, user, *args, **kwargs)
            return inner

        def get_queryset_wrapper(view_func):
            @wraps(view_func, assigned=available_attrs(view_func))
            def inner(self, *args, **kwargs):
                qs = view_func(self, *args, **kwargs)
                if hasattr(qs.model, '_permission_logics'):
                    permission = perm
                    for logics in qs.model._permission_logics:
                        qs = qs.filter(logics.list_filter(self.request.user, permission))
                return qs.distinct()
            return inner

        if hasattr(cls, 'dispatch'):
            cls.dispatch = dispatch_wrapper(cls.dispatch)
        if hasattr(cls, 'get_queryset'):
            cls.get_queryset = get_queryset_wrapper(cls.get_queryset)
        return cls

    return wrapper


def get_object_from_classbased_instance(
        instance, queryset, request, *args, **kwargs):
    """
    Get object from an instance of classbased generic view

    Parameters
    ----------
    instance : instance
        An instance of classbased generic view
    queryset : instance
        A queryset instance
    request : instance
        A instance of HttpRequest

    Returns
    -------
    instance
        An instance of model object or None
    """
    # initialize request, args, kwargs of classbased_instance
    # most of methods of classbased view assumed these attributes
    # but these attributes is initialized in ``dispatch`` method.
    instance.request = request
    instance.args = args
    instance.kwargs = kwargs

    # get queryset from class if ``queryset_or_model`` is not specified
    if not queryset:
        if hasattr(instance, 'get_queryset'):
            queryset = instance.get_queryset()
        elif hasattr(instance, 'queryset'):
            queryset = instance.queryset
        elif hasattr(instance, 'model'):
            queryset = instance.model._default_manager.all()

    # get object
    if not issubclass(type(instance), SingleObjectMixin):
        obj = None
    elif hasattr(instance, 'get_object'):
        try:
            obj = instance.get_object(queryset)
        except AttributeError as e:
            # CreateView has ``get_object`` method but CreateView
            # should not have any object before thus simply set
            # None
            if isinstance(instance, BaseCreateView):
                obj = None
            else:
                raise e
    elif hasattr(instance, 'object'):
        obj = instance.object
    else:
        obj = None
    return obj
