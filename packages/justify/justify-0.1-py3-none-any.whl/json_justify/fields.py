"""
This file configures valid fields That are in
Valid json configurations
"""

from json_justify.utils import PlaceHolder
from inspect import isclass
from json_justify.validators import Invalid
import json_justify.jason


class Field(object):
    """
    This is field which is used subset
    """

    def __init__(self, field_name, validators=None):
        """
        The Basic Field object Which should be instanciated
        By every Field one create and also by custom fields
        
        Args:
            field_name (str): field name in object
            validators (None, optional): Data validators
        """
        self.field_name = Keyname(field_name)
        self.error_messages = dict()
        if validators is not None and not isinstance(validators, list):
            raise Invalid("validators: should be None or list type")
        self.validators = validators

    def __str__(self):
        """This is added to give a string Representation
        of Field in different places
        """
        return '<{0}>'.format(self.__class__.__name__)

    __repr__ = __str__

    @property
    def data(self):
        """
        This is used to get field data
        :return: data of field
        """
        return self._data

    @data.setter
    def data(self, value):
        self._data = value if value is not None else PlaceHolder()

    @data.deleter
    def data(self):
        raise Invalid("Cannot Delete data attribute")

    def register_error(self, key,value):
        """This Function is used to register error
        of the fields which is usually done by the
        validaors to reetister error
        
        Args:
            message (str): Description of the message
        """
        self.error_messages[key] = value

    def __call__(self, field_object):
        """
        This is called to validate
        :param field_object:
        :return:
        """
        self.field_object = field_object
        if str(self.field_name) in self.field_object:
            self.data = self.field_object._mapped_data[str(self.field_name)]
            self._validate()
        else:
            raise Invalid(str(self.field_name) + "is not present in object" + self.__class__.__name__)

    def _validate(self, *args, **kwargs):
        """
        This function is used to validate field
        it should be overided by the instanciated class
        :return:
        """
        pass


class String(Field):
    """
    This is Basic String Field
    """

    def _validate(self):
        """
        The validator is used to
        :return:
        """
        if isinstance(self.data, str):
            if self.validators is not None:
                for check in self.validators:
                    check(self.field_object, self)
            else:
                return True
        else:
            raise Invalid("These are Invalid Field")


class Number(Field):
    """
    This Field is used to Create Numerical Fields
    """
    def _validate(self):
        """
        This is used to validate the data 
        """
        if isinstance(self.data, int) or isinstance(self.data, float):
            if self.validators is not None:
                for check in self.validators:
                    check(self.field_object, self)
            else:
                return True
        else:
            raise Invalid('This booleanfield is Invalid')


class Boolean(Field):
    """
    This is Boolean Field
    """

    def _validate(self):
        """
        The validate option
        :return:
        """
        if isinstance(self.data, bool):
            if self.validators:
                for check in self.validators:
                    check(self.field_object, self)
            else:
                return True
        else:
            raise Invalid("Data should be boolean type")


# TODO: Need to add n-d dimentional array support
class Array(Field):
    """
    This is Array Field This is Simple one with simple
    literals as their items like
    """
    def __init__(self, field_name, min_len=-1, max_len=-1,
                 js_model=None, validators=None, seq_validators=None):
        """This is addition of functionality of function
        in init function
        
        Args:
            field_name (TYPE): Description
            validators (None, optional): Description
        """
        super(Array, self).__init__(field_name, validators)

        _t_ckeck = [cls for cls in (validators, seq_validators, js_model) if cls is not None]
        _t_ckeck = len(_t_ckeck)
        if _t_ckeck > 1:
            raise ValueError("you can use only one at a time from validators, "
                             "seq_validators and js_model")

        if seq_validators is not None and not isinstance(seq_validators, list):
            raise Invalid("param seq_validators: should be a list type")

        self.seq_validators = seq_validators

        if js_model is not None and isclass(js_model) and not issubclass(js_model, json_justify.jason.JsonManager):
            raise Invalid("Please provide a class that subclasses JsonManager")

        self.js_model = js_model

        if self.seq_validators is not None:
            self.min_len = self.max_len = len(self.seq_validators)
        else:
            self.min_len = min_len
            self.max_len = max_len

    def __call__(self, field_object):
        """A overiding and providing a new implementation for the
        array field
        
        Args:
            field_object (Field): A field controlled array
        """
        if not isinstance(field_object, json_justify.jason.JsonManager):
            raise ValueError("field object to filed should be instance of JsonManager")

        self.field_object = field_object
        if str(self.field_name) in self.field_object:
            dat = self.field_object._mapped_data[str(self.field_name)]
            if not isinstance(dat, list):
                raise Invalid("Array should Be list")
            if (len(dat) < self.min_len or 
                    self.js_model is None and
                    self.max_len != -1 and len(dat) > self.max_len):
                raise Invalid("Invalid Length of Array Found")
            for index, data in enumerate(dat):
                self.data = data
                self._validate(index)
        else:
            raise Invalid("Array is invalid")

    def _validate(self, index):
        
        if self.validators is not None:
            for check in self.validators:
                check(self.field_object, self)

        elif self.seq_validators is not None:
            check = self.seq_validators[index]
            check(self.field_object, self)

        elif self.js_model is not None:
            js = self.js_model
            js = js(data=self.data, _child_hook=True)
            js.is_valid()
        else:
            return True


class Keyname(object):

    """This is used to assing key name in the field of the json
    """
    
    def __init__(self, key, prefix=None):
        if prefix is not None and isinstance(prefix, str) and bool(prefix.strip()):
            self._prefix = prefix.strip()
        else:
            self._prefix = ''

        if isinstance(key, str) and bool(key.strip()):
            self._key = key.strip()
        else:
            raise TypeError("key of json should be of string Type")

    def __str__(self):
        return str(self._prefix + self._key)

    def __repr__(self):
        return str(self._prefix + self._key)