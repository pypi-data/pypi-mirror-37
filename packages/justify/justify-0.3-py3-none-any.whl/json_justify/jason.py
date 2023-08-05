from json_justify.validators import Invalid
import json_justify.fields as fields
from inspect import isclass
from json import dumps

class InvalidMachiene(ValueError):
    """
    This is raised when you register invalid mahiene
    """

    def __init__(self, message):
        """Initialize the class

        Args:
            message (str): message to provide in the container
        """
        super(InvalidMachiene, self).__init__(message)


class InvalidContainer(ValueError):

    """This Class is used to Create Exception when
    Invalid Json is Provided to Manager or some
    invalid activity is encountered by Manager
    """

    def __init__(self, message):
        """Initializing the class

        Args:
            message (str): Message to be displayed in 
            stack trace when want this error)
        """
        super(InvalidContainer, self).__init__(message)


class JsonManager(object):

    """This is the main json field which ultimately
    any progarm will subclass to make it
    possible to create Json classes

    Attributes:
        data (TYPE): Description
        otk_token (TYPE): Description

    """
    Object = dict
    integral_types_list = [str, bool, float, int, list]

    def __init__(self, data , allow_extra=False, _child_hook = False):
        """This function will create some attris for own
        need and if app variable is provided then it will
        use this app to create global protections
        """
        self.data = data
        self._render_funcs = set()
        self._attris_funcs = list()
        self.static = {}
        self._error_data = {}
        self._mapped_data = {}
        self.allow_extra = allow_extra
        self.child = _child_hook
        self.add_render_machiene(self.generate_otk_token)
        self.setup_fields()
        self._get_render_machienes()

    def __contains__(self, value):
        """A membership operator implementation

        Args:
            value (key): key in _fields

        Returns:
            bool: True or False
        """
        _return = value in self._field_dict
        return _return

    def __getitem__(self, value):
        """A item getter one of protocol 

        Args:
            value (key): Key of field dict

        Returns:
            value: Value of key dict
        """
        return self._field_dict[value]

    def __setitem__(self, key, value):
        """A item Setter of protocol

        Args:
            key (str)  : key of dict
            value (any): Value of key
        """
        if not isinstance(value, fields.Field):
            raise TypeError("value set should be instance of Field class")
        self._field_dict[key] = value

    def __iter__(self):
        dct = self.setup_fields()
        return iter(dct)

    def __str__(self):
        """A string Representation of object

        Returns:
            str: Representation
        """
        return "<{0} of JsonManager>".format(self.__class__.__name__)

    def __len__(self):
        """This will used to get length of class

        Returns:
            int: Length of field dict
        """
        return len(self._field_dict)

    __repr__ = __str__

    def items(self):
        """This is the implementation of items

        Returns:
            list: a tuple to access
        """
        sge = []
        for key in self:
            sge.append((key, self[key]))
        return sge

    def is_object(self, value):
        """This class is used to check if it is
        dir which is standard key value pair or not

        Args:
            value (any): Value to validate

        Returns:
            bool: True if dir else Flase
        """
        return isinstance(value, self.Object)

    @property
    def child(self):
        return self._child_hook

    @child.setter
    def child(self, value):
        if not isinstance(value, bool):
            raise ValueError("Plese child parameter is bool")
        self._child_hook = value

    def setup_fields(self):
        """This function will setup or say filter
        fields form all value in object

        Returns:
            dict: dict of filtered obj
        """
        dct = {str(clas) or str(getattr(self, clas).field_name): getattr(self, clas)
               for clas in dir(self) if
               isinstance(getattr(self, clas), fields.Field) or
               isclass(getattr(self, clas)) and
               not str(clas).startswith('_') and
               issubclass(getattr(self, clas), JsonManager)}
        self._field_dict = dct
        return dct

    def setup_json(self):
        """This is function which will be used to 
        setup form if data is not provided in json
        format
        """
        if self.data is not None:
             self._set_data(data = self.data)
        else:
            self.regester_error("Error","Data Value is Null")
            raise Invalid("Please Provide Data To Function")  

    def _set_data(self, data=None):
        """This function is called to setup the
        Field data attribute according to field
        type

        Args:
            data (dict): A dict which is python like
            object in javascript a little bit pythonic but
            doesnt make any difference in process
        """
        if not isinstance(data, dict):
            return
        self.data = data

        self._mapped_data = {key: self[key]
                             for key in self if key not in self.data}
        if len(self._mapped_data) > 0:
            self.regester_error("Error","Not All fields available")
            raise Invalid("Please Provide A valid json with all fields")
        elif len(self._mapped_data) == 0:
            if not self.allow_extra and len(self.data) > len(self):
                self.regester_error("Error","Extra fields not Accepted")
                raise Invalid("Extra Field Not Excepted")
            self._mapped_data = self.data
        else:
            self.regester_error("Error","Invaid Json")
            raise Invalid("Invalid json")

    def _get_render_machienes(self):
        if "render_machienes" in dir(self):
            machiene = getattr(self,"render_machienes")
            if not isinstance(machiene, tuple):
                raise ValueError(str(machiene) + "Should be a tuple type")
            for func in machiene:
                self.add_render_machiene(func)

    def integral_types(self,data):
        """This is used to check if field data is
        in integral types or not
        
        Args:
            fields (any): any field data
        """
        for bsclas in self.integral_types_list:
            if isinstance(data,bsclas):
                return True
        return False

    def  is_valid(self):
        """This is the manage function which will run
        Field's validate function in for loop
        """
        # TODO: Add setup json inside try block and if json is not
        # Todo: provided Then Reutrn False

        try:
            self.setup_json()
            for field_key, field in self.items():
                # TODO: Add check for self._mapped data attribute check
                data = self._mapped_data.get(field_key)
                if (self.is_object(data) and
                isclass(field) and
                issubclass(field, JsonManager)):
                    js = field(data = data, _child_hook = True)
                    js.is_valid()
                else:
                    # You can also set data directly but dont
                    # do it directly its system specifiv
                    field(self)
        except Invalid as e:
            if self.child:
                raise Invalid(str(e))
            else:
                self.regester_error("Error",str(e))
                return False
        return True

    def __call__(self):
        """just a way to make it callable
        """
        return self.is_valid()


    def regester_attris(self, func):
        """This function is used to register own functions
        which will run in creation of dictionary

        Args:
            func (func): The function to run when 
            class attributes one want to register  
        """
        if not callable(func):
            raise InvalidMachiene("Registered Attris should be callable")
        self._attris_funcs.append(func)

    def regester_error(self, name, value):
        """This is used to regester error to the object
        and used to regester validation Error

        Args:
            error_obj (TYPE): Description
        """
        self._error_data[name] = value

    def generate_otk_token(self):
        """This method should be reimplemented in the class who will
        instanciate this
        
        Returns:
            tuple: authentication token
        """
        return ('auth_token', 'token')

    def _setup_attris(self):
        """This method is used to setup attris whirender_jsonch
        can be used directly i_retu_returnrnnside json creation
        """
        st = keymapper(self._attris_funcs)
        self.static = st

    def render_json(self):
        """This function is used as a master key to create
        json with registered rendered function and send it
        back as response 
        """
        ren = self._run_render_machines()
        self._setup_attris()
        st = self.static
        return dumps(addupdict(st,ren))


    def add_render_machiene(self, func):
        """The function which will run 

        Args:
            func (callable): A callable
        """
        if not callable(func):
            raise InvalidContainer("render machiene should be callable")
        self._render_funcs.add(func)

    def _run_render_machines(self):
        """This function will be used to setup
        fun render function and then creation
        of sendable json
        """
        _return = keymapper(self._render_funcs)
        return _return

    def json_or_error(self):
        """
        json_or_error function should be to get json or error
        -json and returned to system and then rendered accordingly
        :return:
        """
        if self.is_valid():
            return self.data
        else:
            return self._error_data

def keymapper(dict_like):
    """This function is used to take a function 
    and then reutrn dict that will be used later
    
    Args:
        dict_like (list,set): A dict that will be used for
        the later functionalities like mapping
        this is basically used to create a mapping
        of render and attris function functionaliies
        creation
    """
    _return = {}
    for func in dict_like:
        ret = func()
        if len(ret) is 1:
            name = func.__name__
            _return[name] = func()[0]
        elif len(ret) is 2:
            _return[ret[0]] = ret[1]
        else:
            raise ValueError("you must return a tuple or func")
    return _return


def addupdict(*args):
    _storage = {}
    for arg in args:
        if not isinstance(arg, dict):
            raise ValueError("All Values Should Be dict")
        for key, value in arg.items():
            _storage[key] = value
    return _storage

def render_factory(js, render_tup):
    if not isinstance(js, JsonManager):
        raise ValueError("parameter js should be instance of JsonManager")

    for render in render_tup:
        js.add_render_machiene(render)
