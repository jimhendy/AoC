import pytest

from tools.binary_search import binary_search
from tools.errors import BinarySearchError


class TestBinarySearch:
    # Returns the smallest possible value x such that func(x) is True.
    def test_smallest_value(self):
        def is_positive(n):
            return n > 0

        result = binary_search(is_positive)
        assert result == 1

    # Returns the correct output for a simple function like is_positive(n).
    def test_simple_function(self):
        def is_positive(n):
            return n > 0

        result = binary_search(is_positive)
        assert result == 1

    # Returns the correct output for a custom function with a range of values.
    def test_custom_function(self):
        def custom_func(x):
            return x % 2 == 0

        result = binary_search(custom_func, lower=10, upper=13)
        assert result == 10

    # Raises an AssertionError if upper is provided and func(lower) is equal to func(upper).
    def test_assertion_error(self):
        def equal_func(x):
            return x == 5

        with pytest.raises(BinarySearchError):
            binary_search(equal_func, lower=5, upper=5)

    # Returns the correct output when the function returns True for the lower bound.
    def test_lower_bound(self):
        def lower_bound_func(x):
            return x == 0

        result = binary_search(lower_bound_func, lower=0, upper=10)
        assert result == 0

    # Returns the correct output when the function returns True for the upper bound.
    def test_upper_bound(self):
        def upper_bound_func(x):
            return x == 10

        result = binary_search(upper_bound_func, lower=0, upper=10)
        assert result == 10

    # An error is raised if we can't find a suitable upper as it returns the same value from the function as the lower bound
    def test_lower_bound_not_zero(self):
        def is_positive(n):
            return n > 0

        with pytest.raises(BinarySearchError):
            binary_search(is_positive, lower=10)

    # Returns the correct output when the upper bound is not None.
    def test_upper_bound_not_none(self):
        def is_positive(n):
            return n > 0

        result = binary_search(is_positive, upper=100)
        assert result == 1

    # Returns the correct output when the function is a lambda function.
    def test_lambda_function(self):
        result = binary_search(lambda x: x % 2 == 0)
        assert result == 0

    # Returns the correct output when the function is a built-in function.
    def test_builtin_function(self):
        def is_even(n):
            return n % 2 == 0

        result = binary_search(is_even)
        assert result == 0

    # Returns the correct output when the function returns True for the middle value.
    def test_middle_value(self):
        def is_middle(n):
            return n >= 5

        result = binary_search(is_middle, lower=0, upper=10)
        assert result == 5

    # Returns the correct output when the function returns True for the first value in the range.
    def test_first_value(self):
        def is_first(n):
            return n == 0

        result = binary_search(is_first, lower=0, upper=10)
        assert result == 0

    # Returns the correct output when the function returns True for the last value in the range.
    def test_last_value_true(self):
        def is_positive(n):
            return n == 10

        result = binary_search(is_positive, lower=0, upper=10)
        assert result == 10

    # Raises an error when the function returns True for the first and last value in the range.
    def test_all_values_true(self):
        def is_positive(n):
            return n > 0

        with pytest.raises(BinarySearchError):
            binary_search(is_positive, lower=1, upper=10)

    # Returns the correct output when the function returns False for all values in the range.
    def test_all_values_false(self):
        def is_positive(n):
            return n > 0

        with pytest.raises(BinarySearchError):
            binary_search(is_positive, lower=-10, upper=-1)

    def test_func_returns_true_at_lower_bound(self):
        def func(x):
            return x == 0

        result = binary_search(func)
        assert result == 0

    def test_func_returns_true_at_upper_bound(self):
        def func(x):
            return x == 10

        result = binary_search(func, upper=10)
        assert result == 10

    def test_func_returns_true_within_range(self):
        def func(x):
            return x > 5

        result = binary_search(func, lower=0, upper=10)
        assert result == 6

    def test_func_returns_true_within_range_reversed(self):
        def func(x):
            return x > -5

        result = binary_search(func, lower=-10, upper=-1)
        assert result == -4

    def test_func_returns_true_for_range_with_negative_values(self):
        def func(x):
            return x >= -5

        result = binary_search(func, lower=-10, upper=-1)
        assert result == -5
