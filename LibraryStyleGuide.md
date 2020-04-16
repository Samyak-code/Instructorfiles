# MIT RACECAR-MN Library Style Guide

Please adhere to this style guide when contributing to the `racecar_core` and `racecar_utils` libraries of the RACECAR-MN platform. The library files can be found in the [Student](https://github.com/MITLLRacecar/Student/tree/develop/library) repository.

In general, refer to [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python style.

## Summary

Before submitting a pull request, ask yourself:

1. Have I run Black and manually enforced 88 characters per line in docstrings?
2. Have I added sufficient comments such that students could understand my code (especially important in `racecar_utils`)?
3. Do all of my public methods have docstrings following the requirements specified in this document?
4. Have I verified that my documentation properly renders locally with Sphinx?
5. Have I followed the naming conventions in this document, especially relating to private functions?
6. Do all of my public methods verify that they have received valid arguments with relevant `assert`s?

## Auto Formatting

Every library file should be formatted with [Black](https://pypi.org/project/black/) before committing. You can configure VS code to automatically run Black when you press `Shift + Alt + F` (Windows). Black enforces PEP 8 formatting and enforces additional consistency for formatting decisions on which PEP 8 does not take a position.

Black enforces 88 characters per line for code but does not enforce a character limit in docstrings. We have chosen to manually extend this limit to docstrings as well, so **please manually format docstrings to 88 characters by hand**. In VS code you can [add a ruler](https://stackoverflow.com/questions/29968499/vertical-rulers-in-visual-studio-code) at 88 characters to help with this.

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

- If a `racecar_core` module has a function which must be called once per frame, name this function `__update` and call it in `Racecar.__update_modules`.

## Asserts

A public method should make no assumptions about any arguments. If anything must be true about an argument, verify it with an `assert`.

For example:

- For an `enum` parameter, include an `isinstance` `assert` to check that the parameter is a member of the correct `enum` .
- For a `tuple` or `list` parameter with a certain shape, include an `assert` to check that shape.
- Far a number parameter, include an `isinstance(x, numbers.Number)` `assert` to check that the parameter is a number.
- For a number parameter that should be within certain bounds, include an `assert` to check those bounds.

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

1. **Input**: human-readable docstrings in library files.
2. **[Doxypypy](https://pypi.org/project/doxypypy/)**: Converts docstrings to a doxygen-friendly format.
3. **[Doxygen](http://doxygen.nl/)**: Extracts semantics from functions, classes, and docstrings.
4. **[Breathe](https://pypi.org/project/breathe/)**: Converts doxygen output into a format understood by Sphinx.
5. **[Sphinx](https://pypi.org/project/Sphinx/)**: Generates documentation for Read the Docs.
6. **[Read the Docs](https://readthedocs.org/)**: Hosts and automatically generates documentation on each push to the `master` branch of the `Student` repository.

The parsing in some steps of this pipeline are quite fragile, so you **must adhere to the following requirements exactly to avoid catastrophic errors** is the output documentation.

Every public function should contain a docstring with the following pieces, in the following order:

- **Brief**: A one line summary of the function. This must be exactly one line.
- **Args**: Specify each parameter of the function, using the format `param name: (type) description of parameter`. If the function does not take any arguments, do not include this section.
- **Returns**: Specify the type in parenthesis, then describe the return value. If the function does return anything, do not include this section.
- **Note** (optional): Use this section to include any relevant notes about the function.
- **Warning** (optional): Use this section to describe any potential dangers associated with the function.
- **Example**: A simple example of the function being used. Please include this for every function. This must go last, unless the example contains a colon (see "Critical Notes" below).

Here is an example docstring for the `Controller.get_joystick` method.

```python
"""
Returns the position of a certain joystick as an (x, y) tuple.

Args:
    joystick: (Joystick enum) Which joystick to check.

Returns:
    (float, float) The x and y coordinate of the joystick, with
    each axis ranging from -1.0 (left or down) to 1.0 (right or up).

Note:
    The parameter must be an associated value of the Joystick enum,
    which is defined in the Controller module.

Example:
    # x and y will be given values from -1.0 to 1.0 based on the position of
    # the left joystick
    x, y = rc.controller.get_joystick(rc.controller.Joystick.LEFT)
"""
```

### Critical Notes

Not following these can break the pipeline.

- Every section except the `Brief` can extend to multiple lines, but **later lines must contain more than one word**.
- Each section header must be on its own line and end in a colon.
- If the `Example` section contains a colon (such as after a `def` or `if` ), then this section must be placed directly after the brief and followed directly by `Args`. If the `Example` is not followed by `Args`, `Returns` will be incorrectly included as part of the example.

### Additional Notes

Please follow these for consistency.

- End each section and each parameter description with a period.
- Capitalize the beginning of each section and each parameter description.

### Reasoning

Good documentation is one of the most important steps in making our library accessible to student. The documentation pipeline saves time and ensures that our public documentation is always up to date. It is helpful for the raw docstrings to be human-readable too.
