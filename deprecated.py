class TextEncoder(type):
    """
    A metaclass that enforces the implementation of `encode` and `decode` methods in derived classes.

    The methods `encode` and `decode` must be callable, take `self` and `text` as parameters, and return a string.
    """

    def __new__(cls, name, bases, dct):
        """
        Creates a new class ensuring it has `encode` and `decode` methods.

        Args:
            cls (type): The metaclass itself.
            name (str): The name of the class being created.
            bases (tuple): The base classes of the class being created.
            dct (dict): The dictionary containing the class attributes.

        Returns:
            type: The newly created class.

        Raises:
            TypeError: If `encode` or `decode` methods are missing, not callable, or do not have the correct signature.
        """
        if 'encode' not in dct or 'decode' not in dct:
            raise TypeError(f"Class {name} must implement both encode and decode methods")

        if not callable(dct['encode']) or not callable(dct['decode']):
            raise TypeError(f"Both encode and decode must be callable")

        check_methods = ['encode', 'decode']
        for method in check_methods:
            signature = inspect.signature(dct[method])
            expected_params = ['self', 'text']
            params = list(signature.parameters.keys())
            if expected_params != params or signature.return_annotation != str:
                raise TypeError(f"Method '{method}' must take 'self' and 'text' parameters and return a string")

        return super().__new__(cls, name, bases, dct)