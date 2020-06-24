# MIT RACECAR-MN Library Style Guide

Please adhere to this style guide when contributing to the `racecar_core` and `racecar_utils` libraries of the RACECAR-MN platform. The library files can be found in the [Student](https://github.com/MITLLRacecar/Student/tree/develop/library) repository.

In general, refer to [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python style.

## Summary

Before submitting a pull request, ask yourself:

1. Have I run Black and manually enforced 88 characters per line in docstrings?
1. Have I added sufficient comments such that students could understand my code (especially important in `racecar_utils`)?
1. Do all of my public methods have docstrings following the requirements specified in this document?
1. Have I verified that my documentation properly renders locally with Sphinx?
1. Have I followed the naming conventions in this document, especially relating to private functions?
1. Do all of my public methods include type hints as specified in [PEP 484](https://www.python.org/dev/peps/pep-0484/)?
1. Do all of my public methods verify that they receive valid arguments with `assert`s when necessary?

## Auto Formatting

Every library file should be formatted with [Black](https://pypi.org/project/black/) before committing. You can configure VS code to automatically run Black when you press `Shift + Alt + F` (Windows). Black enforces PEP 8 formatting and enforces additional consistency for formatting decisions on which PEP 8 does not take a position.

Black enforces 88 characters per line for code but does not enforce a character limit in docstrings. We have chosen to manually extend this limit to docstrings as well, so **please manually format docstrings to 88 characters by hand**. In VS code you can [add a ruler](https://stackoverflow.com/questions/29968499/vertical-rulers-in-visual-studio-code) at 88 characters to help with this.

Black does not automatically remove trailing whitespace, so **please remove trailing whitespace by hand**. In VS code, [this extension](https://marketplace.visualstudio.com/items?itemName=ybaumes.highlight-trailing-white-spaces) will highlight trailing white space.

### Reasoning

Black is an uncompromising formatter which enforces greater consistency than other popular Python formatters. Consistent formatting improves readability. Without extending the 88 character limit to docstrings, much of the benefit of a character limit is lost.

## Naming

Please use the following naming conventions:

- **Classes**: `PascalCase`
- **Functions**: `snake_case`
- **Member constants**: `ALL_CAPITAL`
- **Member variables**: `snake_case`
- **Local constants**: `ALL_CAPITAL`
- **Local variables**: `snake_case`

Every method and member variable of a class which is not part of the public interface should be made "private" by prepending two underscores. For example, the `Controller` class contains the `__was_down` member variable and the `__convert_trigger_value` method.

### Reasoning

Consistent naming of class member variables and methods helps users remember those names. Prepending two underscores for private functions ensures that users do not accidentally call private functions.

### Special functions

If a `racecar_core` module has a function which must be called once per frame, name this function `__update` and call it in `Racecar.__update_modules`.

## Type hints

The parameters and return type of every public method must be annotated with type hints, as specified in [PEP 484](https://www.python.org/dev/peps/pep-0484/).  Use [nptyping](https://pypi.org/project/nptyping/) for NumPy types.

### Reasoning

Type hints are incorporated into the documentation pipeline to automatically provide type information in our [online documentation](https://mitll-racecar.readthedocs.io). This helps students better understand the inputs and outputs of each function.  Type hints also allow students to check their code with a static type checker such as [mypy](http://mypy-lang.org/), helping them identify mistakes early on.

## Asserts

A public method should make no assumptions about each argument except that it is of the type specified by the type hint. If anything else must be true about an argument, verify it with an `assert`. For example, if a float parameter should be in the range [0, 1], verify that the argument falls in this range with an assert.

Each `assert` should return a helpful error message if it fails. The target audience for these error messages are users of the library who are not familiar with its inner workings.

### Reasoning

Since users of our library are often students who are relatively new to Python, we should assume that they will sometimes call library methods with invalid arguments. It is helpful to immediately receive a meaningful error message in these cases.

## Commenting

We use "commenting" to refer to the inline `#` comments which explain how code works (ie implementation comments). This is distinct from "documentation" (ie interface comments), which we use to refer to class, function, and module docstrings.

All functions in `racecar_utils` should be heavily commented such that any student can understand every function. This requires far more commenting than is usually recommended in general applications.

Functions in `racecar_core` should be commented well but do not need to be commented as excessively. These comments are primarily intended for other contributors, not students. Pitch them for someone unfamiliar with the project but with moderate Python and ROS background.

### Reasoning

Students should be able to fully understand `racecar_utils` and understand how to write each function on their own. Good commenting in `racecar_core` will help future contributors.

## Documentation

We use the following documentation pipeline to automatically generate and host our [documentation](https://mitll-racecar.readthedocs.io):

1. **Input**: Type hints and Google-style docstrings in library files.
2. **[sphinx.ext.napolean](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html)**: Converts Google-style docstrings to reStructuredText.
3. **[sphinx-autodoc-typehints](https://pypi.org/project/sphinx-autodoc-typehints/)**: Incorporates method type hints into documentation type information.
4. **[sphinx.ext.autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html)**: Pulls documentation from docstrings.
5. **[Sphinx](https://pypi.org/project/Sphinx/)**: Generates html documentation.
6. **[Read the Docs](https://readthedocs.org/)**: Hosts and automatically generates documentation on each push to the `master` branch of the `Student` repository.

Every public function should have a docstring formatted according to the [Google Python Style Guide](https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html) with the following pieces in the following order:

- **Brief**: A one line summary of the function. This must be exactly one line.
- **Args**: Specify each parameter of the function, using the format `param name: description of parameter`. If the function does not take any arguments, do not include this section.
- **Returns**: Describes the value returned by the function. If the function does return anything, do not include this section.
- **Note** (optional): Use this section to include any relevant notes about the function.
- **Warning** (optional): Use this section to describe any potential dangers associated with the function.
- **Example**: A simple example of the function being used. Please include this for every function. In order to be properly formatted, the example header must be followed by two colons (`Example::`) and an empty line.

As an example, here is the docstring for the `Controller.get_joystick` method.

```python
"""
Returns the position of a certain joystick as an (x, y) tuple.

Args:
    joystick: Which joystick to check.

Returns:
    The x and y coordinate of the joystick, with each axis ranging from
    -1.0 (left or down) to 1.0 (right or up).

Note:
    The joystick argument must be an associated value of the Joystick enum,
    which is defined in the Controller module.

Example::

    # x and y will be given values from -1.0 to 1.0 based on the position of
    # the left joystick
    (x, y) = rc.controller.get_joystick(rc.controller.Joystick.LEFT)
"""
```

Please follow these additional guidelines for consistency.

- End each section and each parameter description with a period.
- Capitalize the beginning of each section and each parameter description.

### Reasoning

Good documentation is one of the most important steps in making our library accessible to student. The documentation pipeline saves time and ensures that our public documentation is always up to date. It is helpful for the raw docstrings to be human-readable too.
