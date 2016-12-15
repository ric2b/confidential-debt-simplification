from pytest import raises

from utils.messages.message import Message, DecodeError
from utils.messages.testing_utils import fake_body


class TestMessage:

    def test_init_no_attributes(self):
        with raises(NotImplementedError):
            Message('request')

    def test_init_only_request_parameters(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'request_params': {'a': str}})
        with raises(NotImplementedError):
            test_class('request')

    def test_init_only_response_parameters(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'response_params': {'a': str}})
        with raises(NotImplementedError):
            test_class('request')

    def test_init_all_class_attributes_incorrect_request_params_type(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'request_params': 5,
                                                    'response_params': {'a': str}})
        with raises(TypeError):
            test_class('request')

    def test_init_all_class_attributes_incorrect_response_params_type(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'request_params': {'a': str},
                                                    'response_params': 'hi'})
        with raises(TypeError):
            test_class('request')

    def test_init_correct_class_attributes_no_parameters_given(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'request_params': {'a': str},
                                                    'response_params': {'a': str}})
        with raises(KeyError):
            test_class('request')

    def test_init_correct_class_attributes_parameter_given_of_incorrect_type(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'request_params': {'a': str},
                                                    'response_params': {'a': str}})
        with raises(TypeError):
            test_class('request', a=67)

    def test_init_correct_class_attributes_parameters_given_of_correct_type(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'request_params': {'a': str,
                                                                       'b': int},
                                                    'response_params': {'a': str}})

        my_object = test_class('request', a='hey', b=42)
        assert my_object.a == 'hey'
        assert my_object.b == 42

        with raises(AttributeError):
            print(my_object.c)

    def test_read_message_type(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'request_params': {'a': str},
                                                    'response_params': {'a': str}})

        assert test_class('request', a='hi').message_type == 'request'

    def test_load_no_parameters(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'request_params': {'a': str},
                                                    'response_params': {'a': str}})

        with raises(DecodeError):
            test_class.load('request', fake_body({}))

    def test_load_missing_parameters(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'request_params': {'a': str,
                                                                       'b': int},
                                                    'response_params': {'a': str}})

        with raises(DecodeError):
            test_class.load('request', fake_body({'b': 42}))

    def test_load_incorrect_parameter_types(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'request_params': {'a': str,
                                                                       'b': int},
                                                    'response_params': {'a': str}})

        with raises(DecodeError):
            test_class.load('request', fake_body({'a': 10, 'b': 42}))

    def test_load_correct_parameters(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'request_params': {'a': str},
                                                    'response_params': {'a': str}})

        my_message = test_class.load('request', fake_body({'a': 'hey'}))

        assert my_message.a == 'hey'
        assert my_message.message_type == 'request'

    def test_body_different_types_of_parameters(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'request_params': {'a': str,
                                                                       'b': int,
                                                                       'c': list,
                                                                       'd': dict},
                                                    'response_params': {'a': str}})

        my_message = test_class('request', a='hi', b=42, c=[1, 'a', 3], d={'e': [1]})
        my_recovered_message = test_class.load('request', my_message.dumps())

        assert my_message.a == my_recovered_message.a
        assert my_message.b == my_recovered_message.b
        assert my_message.c == my_recovered_message.c
        assert my_message.d == my_recovered_message.d

        assert my_message.a != my_recovered_message.b
        assert my_recovered_message.c is not None
        assert my_recovered_message.d == {'e': [1]}






