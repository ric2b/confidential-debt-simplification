from pytest import raises

from utils.requests.message import Message, DecodeError
from utils.requests.testing_utils import fake_body


class TestMessage:

    def test_init_no_attributes(self):
        with raises(NotImplementedError):
            Message()

    def test_init_only_message_type(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'message_type': 'test'})
        with raises(NotImplementedError):
            test_class()

    def test_init_only_parameter_types(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'parameter_types': 'test'})
        with raises(NotImplementedError):
            test_class()

    def test_init_all_class_attributes_incorrect_message_type_type(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'message_type': 5,
                                                    'parameter_types': {'a': str}})
        with raises(TypeError):
            test_class()

    def test_init_all_class_attributes_incorrect_parameter_types_type(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'message_type': 'test',
                                                    'parameter_types': 5})
        with raises(TypeError):
            test_class()

    def test_init_correct_class_attributes_no_parameters_given(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'message_type': 'test',
                                                    'parameter_types': {'a': str}})
        with raises(KeyError):
            test_class()

    def test_init_correct_class_attributes_parameter_given_of_incorrect_type(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'message_type': 'test',
                                                    'parameter_types': {'a': str}})
        with raises(TypeError):
            test_class(a=67)

    def test_init_correct_class_attributes_parameters_given_of_correct_type(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'message_type': 'test',
                                                    'parameter_types': {'a': str,
                                                                        'b': int}})
        my_object = test_class(a='hey', b=42)
        assert my_object.a == 'hey'
        assert my_object.b == 42

        with raises(AttributeError):
            print(my_object.c)

    def test_read_message_type(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'message_type': 'test',
                                                    'parameter_types': {'a': str}})

        assert test_class(a='hi').message_type == 'test'

    def test_load_no_parameters(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'message_type': 'test',
                                                    'parameter_types': {'a': str}})

        with raises(DecodeError):
            my_message = test_class.load(fake_body({}))

    def test_load_missing_parameters(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'message_type': 'test',
                                                    'parameter_types': {'a': str,
                                                                        'b': int}})

        with raises(DecodeError):
            my_message = test_class.load(fake_body({'b': 42}))

    def test_load_incorrect_parameter_types(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'message_type': 'test',
                                                    'parameter_types': {'a': str,
                                                                        'b': int}})

        with raises(DecodeError):
            my_message = test_class.load(fake_body({'a': 10, 'b': 42}))

    def test_load_correct_parameters(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'message_type': 'test',
                                                    'parameter_types': {'a': str}})

        my_message = test_class.load(fake_body({'a': 'hey'}))

        assert my_message.a == 'hey'
        assert my_message.message_type == 'test'

    def test_body_different_types_of_parameters(self):
        # Create a new class: Name, Class parents, Class attributes
        test_class = type('TestClass', (Message,), {'message_type': 'test',
                                                    'parameter_types': {'a': str,
                                                                        'b': int,
                                                                        'c': list,
                                                                        'd': dict}})

        my_message = test_class(a='hi', b=42, c=[1, 'a', 3], d={'e': [1]})
        my_recovered_message = test_class.load(my_message.dump())

        assert my_message.a == my_recovered_message.a
        assert my_message.b == my_recovered_message.b
        assert my_message.c == my_recovered_message.c
        assert my_message.d == my_recovered_message.d

        assert my_message.a != my_recovered_message.b
        assert my_recovered_message.c is not None
        assert my_recovered_message.d == {'e': [1]}






