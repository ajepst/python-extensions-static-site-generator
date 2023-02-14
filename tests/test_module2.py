import pytest
import json


@pytest.mark.test_hooks_callbacks_module2
def test_hooks_callbacks_module2(parse):

    # _callbacks = {}

    hooks = parse("hooks")
    assert hooks.success, hooks.message

    callbacks = (
        hooks.assign_to()
        .match(
            {
                "type": "Assign",
                "targets_0_type": "Name",
                "targets_0_id": "_callbacks",
                "value_type": "Dict",
            }
        )
        .exists()
    )
    assert (
        callbacks
    ), "Are you creating a variable called `_callbacks` set equal to an empty dictionary?"


@pytest.mark.test_hooks_register_decorator_module2
def test_hooks_register_decorator_module2(parse):

    # def register(hook, order=0):
    #     def register_callback(func):

    #         return func

    #     return register_callback

    hooks = parse("hooks")
    assert hooks.success, hooks.message

    register = hooks.query("def register(hook, order=0): ??")
    register_exists = register.exists()

    assert (
        register_exists
    ), "Are you defining a function called `register` with the correct arguments?"

    register_callback = register.method("register_callback")
    register_callback_exists = register_callback.exists()

    assert (
        register_callback_exists
    ), "Are you defining a closure called `register_callback` in the `register` function?"

    arguments_exist = register_callback.has_arg("func", 0)
    assert (
        arguments_exist
    ), "Does the `register_callback` function have the correct arguments?"

    returns_func = register_callback.returns("func")
    assert (
        returns_func
    ), "Are you returning `func` from the `register_callback` function?"

    returns_register_callback = register.returns("register_callback")
    assert (
        returns_register_callback
    ), "Are you returning `register_callback` from the `register` function?"


@pytest.mark.test_hooks_callbacks_default_module2
def test_hooks_callbacks_default_module2(parse):

    #         _callbacks.setdefault(hook, {}).setdefault(order, []).append(func)

    hooks = parse("hooks")
    assert hooks.success, hooks.message

    register = hooks.query("def register(hook, order=0): ??")
    register_exists = register.exists()
    assert (
        register_exists
    ), "Are you defining a function called `register` with the correct arguments?"

    register_callback = register.method("register_callback")
    register_callback_exists = register_callback.exists()

    assert (
        register_callback_exists
    ), "Are you defining a closure called `register_callback` in the `register` function?"

    setdefault_calls_exists = (
        register_callback.calls()
        .match(
            {
                "value_func_value_type": "Call",
                "value_func_value_func_value_type": "Call",
                "value_func_value_func_value_func_value_id": "_callbacks",
                "value_func_value_func_value_func_attr": "setdefault",
                "value_func_value_func_value_args_0_id": "hook",
                "value_func_value_func_value_args_1_type": "Dict",
                "value_func_value_func_attr": "setdefault",
                "value_func_value_args_0_id": "order",
                "value_func_value_args_1_type": "List",
                "value_func_attr": "append",
                "value_args_0_id": "func",
            }
        )
        .exists()
    )

    assert (
        setdefault_calls_exists
    ), "Are you you chaining two calls to `setdefault()` on `_callbacks`? Are you passing `hook` and `{}` to the first and `order` and `[]` to the second? Are you chaining a call to `append()` and passing it `func`?"


@pytest.mark.test_hooks_event_hook_module2
def test_hooks_event_hook_module2(parse):

    # def event(hook, *args):
    #     for order in sorted(_callbacks.get(hook, {})):
    #         for func in _callbacks[hook][order]:
    #             func(*args)

    hooks = parse("hooks")
    assert hooks.success, hooks.message

    event = hooks.query("def event(hook, *args): ??")
    event_exists = event.exists()

    assert (
        event_exists
    ), "Are you defining a function called `event` with the correct arguments?"

    first_for_exists = (
        event.for_()
        .match(
            {
                "target_id": "order",
                "iter_type": "Call",
                "iter_func_id": "sorted",
                "iter_args_0_type": "Call",
                "iter_args_0_func_value_id": "_callbacks",
                "iter_args_0_func_attr": "get",
                "iter_args_0_args_0_id": "hook",
                "iter_args_0_args_1_type": "Dict",
            }
        )
        .exists()
    )

    assert (
        first_for_exists
    ), "Do you have a `for` loop, looping through `sorted(_callbacks.get(hook, {})`? Is the current loop value called `order`?"

    second_for_exists = (
        event.for_()
        .match(
            {
                "0_type": "For",
                "0_target_id": "func",
                "0_iter_type": "Subscript",
                "0_iter_value_type": "Subscript",
                "0_iter_value_value_id": "_callbacks",
                "0_iter_value_slice_type": "Index",
                "0_iter_value_slice_value_id": "hook",
                "0_iter_slice_type": "Index",
                "0_iter_slice_value_id": "order",
            }
        )
        .exists()
    )

    assert (
        second_for_exists
    ), "Do you have a nested `for` loop,  looping through `? Is the current loop value called `func`?"

    func_call_exists = (
        event.for_()
        .match(
            {
                "0_body_0_type": "Expr",
                "0_body_0_value_type": "Call",
                "0_body_0_value_func_id": "func",
                "0_body_0_value_args_0_type": "Starred",
                "0_body_0_value_args_0_value_id": "args",
            }
        )
        .exists()
    )

    assert func_call_exists, "Are you calling `func` passing in `*args`?"


@pytest.mark.test_hooks_filter_hook_module2
def test_hooks_filter_hook_module2(parse):

    # def filter(hook, value, *args):
    #     for order in sorted(_callbacks.get(hook, {})):
    #         for func in _callbacks[hook][order]:
    #             value = func(value, *args)
    #     return value

    hooks = parse("hooks")
    assert hooks.success, hooks.message

    filter_call = hooks.query("def filter(hook, value, *args): ??")
    filter_call_exists = filter_call.exists()

    assert (
        filter_call_exists
    ), "Are you defining a function called `filter` with the correct arguments?"

    first_for_exists = (
        filter_call.for_()
        .match(
            {
                "target_id": "order",
                "iter_type": "Call",
                "iter_func_id": "sorted",
                "iter_args_0_type": "Call",
                "iter_args_0_func_value_id": "_callbacks",
                "iter_args_0_func_attr": "get",
                "iter_args_0_args_0_id": "hook",
                "iter_args_0_args_1_type": "Dict",
            }
        )
        .exists()
    )

    assert (
        first_for_exists
    ), "Do you have a `for` loop, looping through `sorted(_callbacks.get(hook, {})`? Is the current loop value called `order`?"

    second_for_exists = (
        filter_call.for_()
        .match(
            {
                "0_type": "For",
                "0_target_id": "func",
                "0_iter_type": "Subscript",
                "0_iter_value_type": "Subscript",
                "0_iter_value_value_id": "_callbacks",
                "0_iter_value_slice_type": "Index",
                "0_iter_value_slice_value_id": "hook",
                "0_iter_slice_type": "Index",
                "0_iter_slice_value_id": "order",
            }
        )
        .exists()
    )

    assert (
        second_for_exists
    ), "Do you have a nested `for` loop,  looping through `? Is the current loop value called `func`?"

    func_call_exists = (
        filter_call.for_()
        .match(
            {
                "0_body_0_type": "Assign",
                "0_body_0_targets_0_id": "value",
                "0_body_0_value_type": "Call",
                "0_body_0_value_func_id": "func",
                "0_body_0_value_args_0_id": "value",
                "0_body_0_value_args_1_type": "Starred",
                "0_body_0_value_args_1_value_id": "args",
            }
        )
        .exists()
    )

    assert (
        func_call_exists
    ), "In the nested `for` loop are you calling `func` and passing in `value` and `*args`? Are you assigning the result back to `value`?"

    returns_value = filter_call.returns("value")
    assert returns_value, "Are you returning `value` from the `filter` function?"
