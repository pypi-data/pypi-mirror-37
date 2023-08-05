# Copyright (c) Microsoft Corporation. All rights reserved.
from .value import to_dprep_value
from typing import Any, List, TypeVar, Optional
import numpy as np


def ensure_expression(value):
    return ValueExpression(value) if not isinstance(value, Expression) else value


def assert_expression(value):
    if not isinstance(value, Expression):
        raise TypeError('An expression was expected, but found a value instead. You can use the expression builders '
                        'in the expressions module to create one.')


def expression_input(fn):
    def ensured_fn(*args):
        args = [args[0]] + [ensure_expression(arg) for arg in args[1:]]
        return fn(*args)

    return ensured_fn


class Expression:
    def __init__(self, underlying_data: Any):
        self.underlying_data = underlying_data

    @expression_input
    def __eq__(self, other: Any) -> 'Expression':
        return InvokeExpression(IdentifierExpression('Value_Equals'), [self, other])

    @expression_input
    def __ne__(self, other: Any) -> 'Expression':
        return NotExpression(InvokeExpression(IdentifierExpression('Value_Equals'), [self, other]))

    def __invert__(self) -> 'Expression':
        return NotExpression(self)

    def __bool__(self):
        raise RuntimeError('Data prep expressions cannot be used in conditional expressions.')


class FunctionSupportingExpression(Expression):
    @expression_input
    def __lt__(self, other: Any) -> 'Expression':
        return InvokeExpression(IdentifierExpression('Value_LT'), [self, other])

    @expression_input
    def __le__(self, other: Any) -> 'Expression':
        return InvokeExpression(IdentifierExpression('Value_LE'), [self, other])

    @expression_input
    def __gt__(self, other: Any) -> 'Expression':
        return InvokeExpression(IdentifierExpression('Value_GT'), [self, other])

    @expression_input
    def __ge__(self, other: Any) -> 'Expression':
        return InvokeExpression(IdentifierExpression('Value_GE'), [self, other])

    @expression_input
    def contains(self, value: Any) -> 'Expression':
        return InvokeExpression(IdentifierExpression('String_Contains'), [self, value])

    @expression_input
    def starts_with(self, value: Any) -> 'Expression':
        return InvokeExpression(IdentifierExpression('String_StartsWith'), [self, value])

    @expression_input
    def ends_with(self, value: Any) -> 'Expression':
        return InvokeExpression(IdentifierExpression('String_EndsWith'), [self, value])

    @expression_input
    def substring(self, start_value: 'IntExpressionLike', length_value: Optional['IntExpressionLike'] = None) -> 'Expression':
        return InvokeExpression(IdentifierExpression('String_Substring'), [self, start_value, length_value])

    def is_null(self) -> 'Expression':
        return InvokeExpression(IdentifierExpression('Value_IsNull'), [self])

    def is_error(self) -> 'Expression':
        return InvokeExpression(IdentifierExpression('Value_IsError'), [self])


class IdentifierExpression(FunctionSupportingExpression):
    def __init__(self, identifier: str):
        super().__init__(to_dprep_value({'Identifier': to_dprep_value(identifier)}))


class ValueExpression(FunctionSupportingExpression):
    def __init__(self, value: Any):
        super().__init__(to_dprep_value({'Value': to_dprep_value(value)}))


class InvokeExpression(FunctionSupportingExpression):
    def __init__(self, function: Expression, arguments: List[Expression]):
        super().__init__(to_dprep_value({
            'Invoke': [function.underlying_data, [a.underlying_data if a is not None else None for a in arguments]]
        }))


class RecordFieldExpression(FunctionSupportingExpression):
    def __init__(self, record_expression: Expression, field_expression: Expression):
        super().__init__(to_dprep_value({
            'RecordField': [record_expression.underlying_data, field_expression.underlying_data]
        }))


class NotExpression(Expression):
    def __init__(self, expression: Expression):
        super().__init__(to_dprep_value({
            'Not': expression.underlying_data
        }))


class AndExpression(Expression):
    def __init__(self, lhs: Expression, rhs: Expression):
        super().__init__(to_dprep_value({
            'And': [lhs.underlying_data, rhs.underlying_data]
        }))


class OrExpression(Expression):
    def __init__(self, lhs: Expression, rhs: Expression):
        super().__init__(to_dprep_value({
            'Or': [lhs.underlying_data, rhs.underlying_data]
        }))


class IfExpression(FunctionSupportingExpression):
    def __init__(self, condition: Expression, true_value: Expression, false_value: Expression):
        super().__init__(to_dprep_value({
            'If': [condition.underlying_data, true_value.underlying_data, false_value.underlying_data]
        }))


StrExpressionLike = TypeVar('StrExpressionLike', Expression, str)
BoolExpressionLike = TypeVar('BoolExpressionLike', Expression, bool)
IntExpressionLike = TypeVar('IntExpressionLike', Expression, int, np.int)
ExpressionLike = TypeVar('ExpressionLike', StrExpressionLike, IntExpressionLike, BoolExpressionLike)


value = IdentifierExpression('value')


def col(name: StrExpressionLike) -> RecordFieldExpression:
    """
    Creates an expression that retrieves the value in the specified column from a record.

    :param name: The name of the column.
    :return: An expression.
    """
    return RecordFieldExpression(IdentifierExpression('row'), ensure_expression(name))


def f_not(expression: Expression) -> Expression:
    """
    Negates the specified expression.

    :param expression: An expression.
    :return: The negated expression.
    """
    return NotExpression(expression)


def f_and(*expressions: List[Expression]) -> Expression:
    """
    Returns an expression that evaluates to true if all expressions are true; false otherwise. This expression
    supports short-circuit evaluation.

    :param expressions: List of expressions, at least 2 expressions are required.
    :return: An expression that results in a boolean value.
    """
    return _reduce_bin_exp(expressions, AndExpression)


def f_or(*expressions: List[Expression]) -> Expression:
    """
    Returns an expression that evaluates to true if any expression is true; false otherwise. This expression
    supports short-circuit evaluation.

    :param expressions: List of expressions, at least 2 expressions are required.
    :return: An expression that results in a boolean value.
    """
    return _reduce_bin_exp(expressions, OrExpression)


def cond(condition: Expression, if_true: Any, or_else: Any) -> Expression:
    """
    Returns a conditional expression that will evaluate an input expression and return one value/expression if it
    evaluates to true or a different one if it doesn't.

    :param condition: The expression to evaluate.
    :param if_true: The value/expression to use if the expression evaluates to True.
    :param or_else: The value/expression to use if the expression evaluates to False.
    :return: A conditional expression.
    """
    true_value = ensure_expression(if_true)
    false_value = ensure_expression(or_else)
    return IfExpression(condition, true_value, false_value)


def _reduce_bin_exp(expressions: List[Expression], expression_ctr: Any) -> Expression:
    if len(expressions) < 2:
        raise ValueError('There need to be at least two expressions, only received {}'.format(len(expressions)))

    prev_exp = expressions[0]
    for exp in expressions[1:]:
        prev_exp = expression_ctr(prev_exp, exp)
    return prev_exp
