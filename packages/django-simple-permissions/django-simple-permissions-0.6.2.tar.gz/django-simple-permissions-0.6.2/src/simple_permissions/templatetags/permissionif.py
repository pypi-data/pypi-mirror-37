# vim: set fileencoding=utf-8 :
"""
permissionif templatetag
"""
from django import template
from django.apps import apps
from django.template import TemplateSyntaxError
from django.template.smartif import infix
from django.template.smartif import IfParser
from django.template.smartif import OPERATORS
from django.template.defaulttags import IfNode, TemplateLiteral
from django.utils.safestring import SafeText


register = template.Library()


def on_operator(context, x, y):
    """
    'on' operator of permission if

    This operator is used to specify the target object of permission
    """
    return x.eval(context), y.eval(context)


def has_operator(context, x, y):
    """
    'has' operator of permission if

    This operator is used to specify the user object of permission
    """
    user = x.eval(context)
    perm = y.eval(context)
    if isinstance(perm, (list, tuple)):
        perm, obj = perm
    else:
        obj = None
    if isinstance(obj, str) or isinstance(obj, SafeText):
        app_label, model_name = obj.split('.')
        model = apps.get_model(app_label=app_label, model_name=model_name)
    else:
        model = type(obj)
    return all([logics.has_perm(user, perm, obj=obj) for logics in model._permission_logics])

# Add 'on' and 'has' operator to existing operators
EXTRA_OPERATORS = {
    'on': infix(20, on_operator),
    'has': infix(10, has_operator),
}
EXTRA_OPERATORS.update(OPERATORS)
for key, op in list(EXTRA_OPERATORS.items()):
    op.id = key


class PermissionIfParser(IfParser):
    """Permission if parser"""
    OPERATORS = EXTRA_OPERATORS
    """use extra operator"""

    def translate_token(self, token):
        try:
            # use own operators instead of builtin operators
            op = self.OPERATORS[token]
        except (KeyError, TypeError):
            return self.create_var(token)
        else:
            return op()


class TemplatePermissionIfParser(PermissionIfParser):
    error_class = TemplateSyntaxError

    def __init__(self, parser, *args, **kwargs):
        self.template_parser = parser
        super(TemplatePermissionIfParser, self).__init__(*args, **kwargs)

    def create_var(self, value):
        return TemplateLiteral(self.template_parser.compile_filter(value), value)


@register.tag('permission')
def do_permissionif(parser, token):
    """
    Permission if templatetag

    Examples
    --------
    ::

        {% permission user has 'write' on object %}
            <p>This user have 'write' permission on {{ object }}</p>
        {% elpermission user has 'read' on object %}
            <p>This user have 'read' permission on {{object}}</p>
        {% else %}
            <p>This user have no permission on {{object}}</p>
        {% endif %}

    or, for creation of new objects:

        {% permission user has 'write' on 'app_label.model_name' %}
            <p>This user have 'write' permission on 'app_label.model_name'</p>
        {% elpermission user has 'read' on 'app_label.model_name' %}
            <p>This user have 'read' permission on 'app_label.model_name'</p>
        {% else %}
            <p>This user have no permission on 'app_label.model_name'</p>
        {% endif %}

    """

    bits = token.split_contents()
    ELIF = "el%s" % bits[0]
    ELSE = "else"
    ENDIF = "end%s" % bits[0]

    # {% if ... %}
    bits = bits[1:]
    condition = do_permissionif.Parser(parser, bits).parse()
    nodelist = parser.parse((ELIF, ELSE, ENDIF))
    conditions_nodelists = [(condition, nodelist)]
    token = parser.next_token()

    # {% elif ... %} (repeatable)
    while token.contents.startswith(ELIF):
        bits = token.split_contents()[1:]
        condition = do_permissionif.Parser(parser, bits).parse()
        nodelist = parser.parse((ELIF, ELSE, ENDIF))
        conditions_nodelists.append((condition, nodelist))
        token = parser.next_token()

    # {% else %} (optional)
    if token.contents == ELSE:
        nodelist = parser.parse((ENDIF,))
        conditions_nodelists.append((None, nodelist))
        token = parser.next_token()

    # {% endif %}
    assert token.contents == ENDIF

    return IfNode(conditions_nodelists)
do_permissionif.Parser = TemplatePermissionIfParser


def replace_builtin_if(replace=False):
    OPERATORS.pop('on', None)
    OPERATORS.pop('has', None)

replace_builtin_if()
