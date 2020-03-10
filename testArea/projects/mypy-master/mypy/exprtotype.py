"""Translate an Expression to a Type value."""

from typing import Optional

from mypy.fastparse import parse_type_string
from mypy.nodes import (
    Expression, NameExpr, MemberExpr, IndexExpr, TupleExpr, IntExpr, FloatExpr, UnaryExpr,
    ComplexExpr, ListExpr, StrExpr, BytesExpr, UnicodeExpr, EllipsisExpr, CallExpr,
    get_member_expr_fullname
)
from mypy.types import (
    Type, UnboundType, TypeList, EllipsisType, AnyType, CallableArgument, TypeOfAny,
    RawExpressionType, ProperType
)


class TypeTranslationError(Exception):
    """Exception raised when an expression is not valid as a type."""


def _extract_argument_name(expr: Expression) -> Optional[str]:
    if isinstance(expr, NameExpr) and expr.name == 'None':
        return None
    elif isinstance(expr, StrExpr):
        return expr.value
    elif isinstance(expr, UnicodeExpr):
        return expr.value
    else:
        raise TypeTranslationError()


def expr_to_unanalyzed_type(expr: Expression, _parent: Optional[Expression] = None) -> ProperType:
    """Translate an expression to the corresponding type.

    The result is not semantically analyzed. It can be UnboundType or TypeList.
    Raise TypeTranslationError if the expression cannot represent a type.
    """
    # The `parent` parameter is used in recursive calls to provide context for
    # understanding whether an CallableArgument is ok.
    name = None  # type: Optional[str]
    if isinstance(expr, NameExpr):
        name = expr.name
        if name == 'True':
            return RawExpressionType(True, 'builtins.bool', line=expr.line, column=expr.column)
        elif name == 'False':
            return RawExpressionType(False, 'builtins.bool', line=expr.line, column=expr.column)
        else:
            return UnboundType(name, line=expr.line, column=expr.column)
    elif isinstance(expr, MemberExpr):
        fullname = get_member_expr_fullname(expr)
        if fullname:
            return UnboundType(fullname, line=expr.line, column=expr.column)
        else:
            raise TypeTranslationError()
    elif isinstance(expr, IndexExpr):
        base = expr_to_unanalyzed_type(expr.base, expr)
        if isinstance(base, UnboundType):
            if base.args:
                raise TypeTranslationError()
            if isinstance(expr.index, TupleExpr):
                args = expr.index.items
            else:
                args = [expr.index]
            base.args = [expr_to_unanalyzed_type(arg, expr) for arg in args]
            if not base.args:
                base.empty_tuple_index = True
            return base
        else:
            raise TypeTranslationError()
    elif isinstance(expr, CallExpr) and isinstance(_parent, ListExpr):
        c = expr.callee
        names = []
        # Go through the dotted member expr chain to get the full arg
        # constructor name to look up
        while True:
            if isinstance(c, NameExpr):
                names.append(c.name)
                break
            elif isinstance(c, MemberExpr):
                names.append(c.name)
                c = c.expr
            else:
                raise TypeTranslationError()
        arg_const = '.'.join(reversed(names))

        # Go through the constructor args to get its name and type.
        name = None
        default_type = AnyType(TypeOfAny.unannotated)
        typ = default_type  # type: Type
        for i, arg in enumerate(expr.args):
            if expr.arg_names[i] is not None:
                if expr.arg_names[i] == "name":
                    if name is not None:
                        # Two names
                        raise TypeTranslationError()
                    name = _extract_argument_name(arg)
                    continue
                elif expr.arg_names[i] == "type":
                    if typ is not default_type:
                        # Two types
                        raise TypeTranslationError()
                    typ = expr_to_unanalyzed_type(arg, expr)
                    continue
                else:
                    raise TypeTranslationError()
            elif i == 0:
                typ = expr_to_unanalyzed_type(arg, expr)
            elif i == 1:
                name = _extract_argument_name(arg)
            else:
                raise TypeTranslationError()
        return CallableArgument(typ, name, arg_const, expr.line, expr.column)
    elif isinstance(expr, ListExpr):
        return TypeList([expr_to_unanalyzed_type(t, expr) for t in expr.items],
                        line=expr.line, column=expr.column)
    elif isinstance(expr, StrExpr):
        return parse_type_string(expr.value, 'builtins.str', expr.line, expr.column,
                                 assume_str_is_unicode=expr.from_python_3)
    elif isinstance(expr, BytesExpr):
        return parse_type_string(expr.value, 'builtins.bytes', expr.line, expr.column,
                                 assume_str_is_unicode=False)
    elif isinstance(expr, UnicodeExpr):
        return parse_type_string(expr.value, 'builtins.unicode', expr.line, expr.column,
                                 assume_str_is_unicode=True)
    elif isinstance(expr, UnaryExpr):
        typ = expr_to_unanalyzed_type(expr.expr)
        if isinstance(typ, RawExpressionType):
            if isinstance(typ.literal_value, int) and expr.op == '-':
                typ.literal_value *= -1
                return typ
        raise TypeTranslationError()
    elif isinstance(expr, IntExpr):
        return RawExpressionType(expr.value, 'builtins.int', line=expr.line, column=expr.column)
    elif isinstance(expr, FloatExpr):
        # Floats are not valid parameters for RawExpressionType , so we just
        # pass in 'None' for now. We'll report the appropriate error at a later stage.
        return RawExpressionType(None, 'builtins.float', line=expr.line, column=expr.column)
    elif isinstance(expr, ComplexExpr):
        # Same thing as above with complex numbers.
        return RawExpressionType(None, 'builtins.complex', line=expr.line, column=expr.column)
    elif isinstance(expr, EllipsisExpr):
        return EllipsisType(expr.line)
    else:
        raise TypeTranslationError()
