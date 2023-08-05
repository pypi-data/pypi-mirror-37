# coding=utf-8
from django.apps import apps


class PermissionLogic(object):
    """
    Abstract permission logic class
    """
    def get_full_permission_string(self, perm):
        """
        Return full permission string (app_label.perm_model)
        """
        if not getattr(self, 'model', None):
            raise AttributeError("You need to use `add_permission_logic` to "
                                 "register the instance to the model class "
                                 "before calling this method.")
        app_label = self.model._meta.app_label
        model_name = self.model._meta.object_name.lower()
        return "%s.%s_%s" % (app_label, perm, model_name)

    def has_perm(self, user_obj, perm, obj=None):
        """
        Check if user have permission (of object)

        Parameters
        ----------
        user_obj : django user model instance
            A django user model instance which be checked
        perm : string
            `app_label.codename` formatted permission string
        obj : None or django model instance
            None or django model instance for object permission

        Returns
        -------
        boolean
            Wheter the specified user have specified permission (of specified
            object).

        .. note::
            Sub class must override this method.
        """
        raise NotImplementedError(
            "'%s' does not override `has_perm(user_obj, perm, obj=None)` "
            "method. Sub class of `PermissionLogic` must override this "
            "method.")


class GeneralPermissionLogic(PermissionLogic):

    def get_user_roles(self, user):
        raise NotImplementedError(
            "'%s' does not override `get_user_roles(user)` method."
            "Sub class of `GeneralPermissionLogic` must override this method.")

    def get_roles_filter(self, perm, obj):
        return getattr(self, 'roles_filter_%s' % perm)(obj) if hasattr(self, 'roles_filter_%s' % perm) else False

    def get_list_filter(self, perm, role_list):
        return getattr(self, 'list_filter_%s' % perm)(role_list) if hasattr(self, 'list_filter_%s' % perm) else None

    def has_perm(self, user_obj, perm, obj=None):
        if obj is None:
            return False
        elif isinstance(obj, str):
            app_label, model_name = obj.split('.')
            model = apps.get_model(app_label=app_label, model_name=model_name)
            return all([logics.object_filter(user_obj, perm) for logics in model._permission_logics])
        else:
            roles = self.get_user_roles(user_obj)
            return bool(roles.filter(self.get_roles_filter(perm, obj)).count())

    def roles_filter(self, obj, perm):
        return self.get_roles_filter(perm if perm is not None else 'read', obj)

    def list_filter(self, user, perm):
        return self.get_list_filter(perm if perm is not None else 'read', self.get_user_roles(user))

    def object_filter(self, user, perm):
        return self.list_filter(user, perm)
