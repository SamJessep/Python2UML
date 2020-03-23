"""Generate a class that represents a nested function.

The class defines __call__ for calling the function and allows access to variables
defined in outer scopes.
"""

from typing import List

from mypy.nodes import Var
from mypyc.common import SELF_NAME, ENV_ATTR_NAME
from mypyc.ir.class_ir import ClassIR
from mypyc.ir.func_ir import FuncIR, FuncSignature, RuntimeArg, FuncDecl
from mypyc.ir.ops import BasicBlock, Return, Call, SetAttr, Value, Environment
from mypyc.ir.rtypes import RInstance, object_rprimitive
from mypyc.irbuild.builder import IRBuilder
from mypyc.irbuild.context import FuncInfo, ImplicitClass
from mypyc.irbuild.util import add_self_to_env
from mypyc.primitives.misc_ops import method_new_op


def setup_callable_class(builder: IRBuilder) -> None:
    """Generates a callable class representing a nested function or a function within a
    non-extension class and sets up the 'self' variable for that class.

    This takes the most recently visited function and returns a ClassIR to represent that
    function. Each callable class contains an environment attribute with points to another
    ClassIR representing the environment class where some of its variables can be accessed.
    Note that its '__call__' method is not yet implemented, and is implemented in the
    add_call_to_callable_class function.

    Returns a newly constructed ClassIR representing the callable class for the nested
    function.
    """

    # Check to see that the name has not already been taken. If so, rename the class. We allow
    # multiple uses of the same function name because this is valid in if-else blocks. Example:
    #     if True:
    #         def foo():          ---->    foo_obj()
    #             return True
    #     else:
    #         def foo():          ---->    foo_obj_0()
    #             return False
    name = base_name = '{}_obj'.format(builder.fn_info.namespaced_name())
    count = 0
    while name in builder.callable_class_names:
        name = base_name + '_' + str(count)
        count += 1
    builder.callable_class_names.add(name)

    # Define the actual callable class ClassIR, and set its environment to point at the
    # previously defined environment class.
    callable_class_ir = ClassIR(name, builder.module_name, is_generated=True)

    # The functools @wraps decorator attempts to call setattr on nested functions, so
    # we create a dict for these nested functions.
    # https://github.com/python/cpython/blob/3.7/Lib/functools.py#L58
    if builder.fn_info.is_nested:
        callable_class_ir.has_dict = True

    # If the enclosing class doesn't contain nested (which will happen if
    # this is a toplevel lambda), don't set up an environment.
    if builder.fn_infos[-2].contains_nested:
        callable_class_ir.attributes[ENV_ATTR_NAME] = RInstance(
            builder.fn_infos[-2].env_class
        )
    callable_class_ir.mro = [callable_class_ir]
    builder.fn_info.callable_class = ImplicitClass(callable_class_ir)
    builder.classes.append(callable_class_ir)

    # Add a 'self' variable to the callable class' environment, and store that variable in a
    # register to be accessed later.
    self_target = add_self_to_env(builder.environment, callable_class_ir)
    builder.fn_info.callable_class.self_reg = builder.read(
        self_target, builder.fn_info.fitem.line)


def add_call_to_callable_class(builder: IRBuilder,
                               blocks: List[BasicBlock],
                               sig: FuncSignature,
                               env: Environment,
                               fn_info: FuncInfo) -> FuncIR:
    """Generates a '__call__' method for a callable class representing a nested function.

    This takes the blocks, signature, and environment associated with a function definition and
    uses those to build the '__call__' method of a given callable class, used to represent that
    function. Note that a 'self' parameter is added to its list of arguments, as the nested
    function becomes a class method.
    """
    sig = FuncSignature(
        (RuntimeArg(SELF_NAME, object_rprimitive),) + sig.args, sig.ret_type)
    call_fn_decl = FuncDecl(
        '__call__', fn_info.callable_class.ir.name, builder.module_name, sig)
    call_fn_ir = FuncIR(call_fn_decl, blocks, env,
                        fn_info.fitem.line, traceback_name=fn_info.fitem.name)
    fn_info.callable_class.ir.methods['__call__'] = call_fn_ir
    return call_fn_ir


def add_get_to_callable_class(builder: IRBuilder, fn_info: FuncInfo) -> None:
    """Generates the '__get__' method for a callable class."""
    line = fn_info.fitem.line
    builder.enter(fn_info)

    vself = builder.read(
        builder.environment.add_local_reg(
            Var(SELF_NAME), object_rprimitive, True)
    )
    instance = builder.environment.add_local_reg(
        Var('instance'), object_rprimitive, True)
    builder.environment.add_local_reg(Var('owner'), object_rprimitive, True)

    # If accessed through the class, just return the callable
    # object. If accessed through an object, create a new bound
    # instance method object.
    instance_block, class_block = BasicBlock(), BasicBlock()
    comparison = builder.binary_op(
        builder.read(instance), builder.none_object(), 'is', line
    )
    builder.add_bool_branch(comparison, class_block, instance_block)

    builder.activate_block(class_block)
    builder.add(Return(vself))

    builder.activate_block(instance_block)
    builder.add(Return(builder.primitive_op(
        method_new_op, [vself, builder.read(instance)], line)))

    blocks, env, _, fn_info = builder.leave()

    sig = FuncSignature((RuntimeArg(SELF_NAME, object_rprimitive),
                         RuntimeArg('instance', object_rprimitive),
                         RuntimeArg('owner', object_rprimitive)),
                        object_rprimitive)
    get_fn_decl = FuncDecl(
        '__get__', fn_info.callable_class.ir.name, builder.module_name, sig)
    get_fn_ir = FuncIR(get_fn_decl, blocks, env)
    fn_info.callable_class.ir.methods['__get__'] = get_fn_ir
    builder.functions.append(get_fn_ir)


def instantiate_callable_class(builder: IRBuilder, fn_info: FuncInfo) -> Value:
    """
    Assigns a callable class to a register named after the given function definition. Note
    that fn_info refers to the function being assigned, whereas builder.fn_info refers to the
    function encapsulating the function being turned into a callable class.
    """
    fitem = fn_info.fitem
    func_reg = builder.add(
        Call(fn_info.callable_class.ir.ctor, [], fitem.line))

    # Set the callable class' environment attribute to point at the environment class
    # defined in the callable class' immediate outer scope. Note that there are three possible
    # environment class registers we may use. If the encapsulating function is:
    # - a generator function, then the callable class is instantiated from the generator class'
    #   __next__' function, and hence the generator class' environment register is used.
    # - a nested function, then the callable class is instantiated from the current callable
    #   class' '__call__' function, and hence the callable class' environment register is used.
    # - neither, then we use the environment register of the original function.
    curr_env_reg = None
    if builder.fn_info.is_generator:
        curr_env_reg = builder.fn_info.generator_class.curr_env_reg
    elif builder.fn_info.is_nested:
        curr_env_reg = builder.fn_info.callable_class.curr_env_reg
    elif builder.fn_info.contains_nested:
        curr_env_reg = builder.fn_info.curr_env_reg
    if curr_env_reg:
        builder.add(SetAttr(func_reg, ENV_ATTR_NAME, curr_env_reg, fitem.line))
    return func_reg
