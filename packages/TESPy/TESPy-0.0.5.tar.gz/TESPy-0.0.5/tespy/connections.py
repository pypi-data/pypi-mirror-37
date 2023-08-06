"""
.. module:: connections
    :synopsis:

.. moduleauthor:: Francesco Witte <francesco.witte@hs-flensburg.de>
"""

import numpy as np
import pandas as pd

from tespy.helpers import (MyConnectionError, data_container, dc_prop, dc_flu,
                           dc_cp)
from tespy.components import components as cmp
from tespy.components import characteristics as cmp_char


class connection:
    """
    creates connection between two components

    - check argument consistency
    - set attributes to specified values

    :param comp1: connections source
    :type comp1: tespy.components.components.component
    :param outlet_id: outlet id at the connections source
    :type outlet_id: str
    :param comp2: connections target
    :type comp2: tespy.components.components.component
    :param inlet_id: inlet id at the connections target
    :type inlet_id: str
    :returns: no return value
    :raises: - :code:`TypeError`, if comp1 and comp2 are not of type
               components
             - :code:`ValueError`, if comp1 and comp2 are the same object
             - :code:`ValueError`, if outlet_id or inlet_id are not allowed
               for ids for comp1 or comp2

    **allowed keywords** in kwargs (also see connections.attr().keys()):

    - m (*numeric*, *ref object*), m0 (*numeric*)
    - p (*numeric*, *ref object*), p0 (*numeric*)
    - h (*numeric*, *ref object*), h0 (*numeric*)
    - T (*numeric*, *ref object*)
    - x (*numeric*)
    - v (*numeric*)
    - fluid (*dict*), fluid_balance (*bool*)
    - design (*list*), offdesign (*list*)

    **(off-)design parameters**

    The specification of values for design and/or offdesign is used for
    automatic switch from design to offdesign calculation: All parameters given
    in 'design', e. g. :code:`design=['T', 'p']`, are unset in any offdesign
    calculation, parameters given in 'offdesign' are set for offdesign
    calculation.

    .. note::
        The fluid balance parameter applies a balancing of the fluid vector on
        the specified conntion to 100 %. For example, you have four fluid
        components (a, b, c and d) in your vector, you set two of them
        (a and b) and want the other two (components c and d) to be a result of
        your calculation. If you set this parameter to True, the equation
        (0 = 1 - a - b - c - d) will be applied.

    **example**

    .. code-block:: python

        from tespy import con
        conn = con.connection(turbine, 'out1', condenser, 'in1', m=10, p=0.05)

    creates connection from turbine to condenser (hot side inlet) and sets
    values for mass flow and pressure

    **improvements**
    """

    def __init__(self, comp1, outlet_id, comp2, inlet_id, **kwargs):

        # check input parameters
        if not (isinstance(comp1, cmp.component) and
                isinstance(comp2, cmp.component)):
            msg = ('Error creating connection.'
                   'Check if comp1, comp2 are of type component.')
            raise TypeError(msg)

        if comp1 == comp2:
            msg = ('Error creating connection. '
                   'Can\'t connect component to itself.')
            raise ValueError(msg)

        if outlet_id not in comp1.outlets():
            msg = ('Error creating connection. '
                   'Specified oulet_id is not valid for component ' +
                   comp1.component() + '. '
                   'Valid ids are: ' + str(comp1.outlets()) + '.')
            raise ValueError(msg)

        if inlet_id not in comp2.inlets():
            msg = ('Error creating connection. '
                   'Specified inlet_id is not valid for component ' +
                   comp2.component() + '. '
                   'Valid ids are: ' + str(comp2.inlets()) + '.')
            raise ValueError(msg)

        # set specified values
        self.s = comp1
        self.s_id = outlet_id
        self.t = comp2
        self.t_id = inlet_id

        self.design = []
        self.offdesign = []

        # set default values for kwargs
        var = self.attr()

        for key in self.attr().keys():
            self.__dict__.update({key: var[key]})

        self.set_attr(**kwargs)

    def set_attr(self, **kwargs):
        """
        sets, resets or unsets attributes of a connection, for the keyword
        arguments, return values and errors see object initialisation
        """
        var = self.attr()
        var0 = [x + '0' for x in var.keys()]

        # set specified values
        for key in kwargs:
            if key in var.keys() or key in var0:
                if (isinstance(kwargs[key], float) or
                        isinstance(kwargs[key], int)):
                    # unset
                    if np.isnan(kwargs[key]) and key not in var0:
                        self.get_attr(key).set_attr(val_set=False)
                        self.get_attr(key).set_attr(ref_set=False)
                    # starting value
                    elif key in var0:
                        self.get_attr(key.replace('0', '')).set_attr(
                                val0=kwargs[key])
                    # set/reset
                    else:
                        self.get_attr(key).set_attr(val_set=True,
                                                    val=kwargs[key],
                                                    val0=kwargs[key])

                # reference object
                elif isinstance(kwargs[key], ref):
                    if key == 'fluid' or key == 'x':
                        print('References for fluid vector and vapour mass '
                              'fraction not implemented.')
                    else:
                        self.get_attr(key).set_attr(ref=kwargs[key])
                        self.get_attr(key).set_attr(ref_set=True)

                # fluid specification
                elif isinstance(kwargs[key], dict):
                    # starting values
                    if key in var0:
                        self.get_attr(key.replace('0', '')).set_attr(
                                val0=kwargs[key])
                    # specified parameters
                    else:
                        self.get_attr(key).set_attr(val=kwargs[key].copy())
                        for f in kwargs[key]:
                            kwargs[key][f] = True
                        self.get_attr(key).set_attr(val_set=kwargs[key])

                # data container specification
                elif isinstance(kwargs[key], data_container):
                    self.__dict__.update({key: kwargs[key]})

                # invalid datatype for keyword
                else:
                    msg = 'Bad datatype for keyword argument ' + str(key)
                    raise TypeError(msg)

            # fluid balance
            elif key == 'fluid_balance':
                if isinstance(kwargs[key], bool):
                    self.get_attr('fluid').set_attr(balance=kwargs[key])
                else:
                    msg = ('Datatype for keyword argument ' + str(key) +
                           ' must be bool.')
                    raise TypeError(msg)

            elif key == 'design' or key == 'offdesign':
                if not isinstance(kwargs[key], list):
                    msg = 'Please provide the design parameters as list!'
                    raise TypeError(msg)
                if set(kwargs[key]).issubset(var.keys()):
                    self.__dict__.update({key: kwargs[key]})
                else:
                    msg = ('Available parameters for (off-)design'
                           'specification are: ' + str(var.keys()) + '.')
                    raise ValueError(msg)

            # invalid keyword
            else:
                msg = 'Connection has no attribute ' + str(key)
                raise ValueError(msg)

    def get_attr(self, key):
        """
        get the value of a connection attribute

        :param key: attribute to return its value
        :type key: str
        :returns:
            - :code:`self.__dict__[key]` if object has attribute key
            - :code:`None` if object has no attribute key
        """
        if key in self.__dict__:
            return self.__dict__[key]
        else:
            print(self.connection(), ' has no attribute \"', key, '\"')
            return None

    def attr(self):
        """
        get the list of attributes allowed for a connection object

        :returns: list object
        """
        return {'m': dc_prop(), 'p': dc_prop(), 'h': dc_prop(), 'T': dc_prop(),
                'x': dc_prop(), 'v': dc_prop(),
                'fluid': dc_flu()}

    def to_flow(self):
        """
        create a list containing the connections fluid information

        :returns: :code:`[mass flow, pressure, enthalpy, fluid vector]`
        """
        return [self.m.val_SI, self.p.val_SI, self.h.val_SI, self.fluid.val]


class bus:
    r"""
    establishes a bus for

    - power in- or output
    - heat in- or output
    - thermal input for combustion chambers

    **available parameters**

    - P: total power/heat of the bus, :math:`{[P]=\text{W}}`

    **characteristic lines**

    - c_char: characteristic line linking each component's factor to its power
      output in reference case (for an example see the tespy_examples
      repository)

     **adding components to a bus**

     - :func:`tespy.connections.bus.add_comps`

    :param label: label for the bus
    :type label: str
    :returns: no return value

    **Improvements**

    - improve architecture (e. g. make it similar to connections)
    """

    def __init__(self, label, **kwargs):

        self.comps = pd.DataFrame(columns=['param', 'P_ref', 'char'])

        self.label = label
        self.P = dc_cp(val=np.nan, val_set=False)
        self.char = cmp_char.characteristics(x=np.array([0, 1, 2, 3]),
                                             y=np.array([1, 1, 1, 1]))

        self.set_attr(**kwargs)

    def set_attr(self, **kwargs):

        self.label = kwargs.get('label', self.label)
        self.P.val = kwargs.get('P', self.P.val)

        if np.isnan(self.P.val):
            self.P.val_set = False
        else:
            self.P.val_set = True

    def get_attr(self, key):
        """
        get the value of a bus attribute

        :param key: attribute to return its value
        :type key: str
        :returns:
            - :code:`self.__dict__[key]` if object has attribute key
            - :code:`None` if object has no attribute key
        """
        if key in self.__dict__:
            return self.__dict__[key]
        else:
            print('Bus ' + self.label + ' has no attribute ' + key + '.')
            return None

    def add_comps(self, *args):
        """
        adds components to a bus

        ci are dicts containing a TESPy component object
        as well as a parameter (P, Q, Q1, TI, ...) and a characteristic line
        char (cmp_char):

        {'c': TESPy component object, 'p': parameter as String,
        'char': TESPy characteristics object}

        **The parameter and characteristic line are optional!!**

        **parameter specfication**
        - You do not need to provide a parameter, if the component only has one
          option for the bus (turbomachines, heat exchangers, combustion
          chamber).
        - For instance, you do neet do provide a parameter, if you want to add
          a cogeneration unit ('Q1', 'Q2', 'TI', 'P').

         **characteristic line specification**
        - If you do not provide a characteristic line at all, TESPy assumes a
          constant factor of 1.
        - If you provide a numeric value instead of a characteristic line,
          TESPy takes this numeric value as a constant factor.
        - Provide a TESPy.characteristic (cmp_char), if you want the factor
          to follow a characteristic line.

        :param args: lists ci containing necessary data for the bus
        :type args: list
        :returns: no return value
        """
        for c in args:
            if isinstance(c, dict):
                if 'c' in c.keys():
                    if isinstance(c['c'], cmp.component):
                        self.comps.loc[c['c']] = [None, np.nan, self.char]
                    else:
                        msg = ('c must be a TESPy component.')
                        raise TypeError(msg)
                else:
                        msg = ('You must provide the component c.')
                        raise TypeError(msg)

                for k, v in c.items():
                    if k == 'p':
                        if isinstance(v, str) or v is None:
                            self.comps.loc[c['c']]['param'] = v
                        else:
                            msg = ('Parameter p must be a String.')
                            raise TypeError(msg)

                    elif k == 'char':
                        if isinstance(v, cmp_char.characteristics):
                            self.comps.loc[c['c']]['char'] = v
                        elif (isinstance(v, float) or
                              isinstance(v, np.float64) or
                              isinstance(v, int)):
                            x = np.array([0, 1, 2, 3])
                            y = np.array([1, 1, 1, 1]) * v
                            self.comps.loc[c['c']]['char'] = (
                                    cmp_char.characteristics(x=x, y=y))
                        else:
                            msg = ('Char must be a number or a TESPy '
                                   'characteristics.')
                            raise TypeError(msg)

                    elif k == 'P_ref':
                        if (v is None or isinstance(v, float) or
                                isinstance(v, np.float64) or
                                isinstance(v, int)):
                            self.comps.loc[c['c']]['P_ref'] = v
                        else:
                            msg = ('Char must be a number or a TESPy '
                                   'characteristics.')
                            raise TypeError(msg)
            else:
                msg = ('Provide arguments as dicts. See the documentation of '
                       'bus.add_comps() for more information.')
                raise MyConnectionError(msg)


class ref:
    r"""
    creates reference object for network parametetrisation

    :param ref_obj: connection to be referenced
    :type ref_obj: tespy.connections.connection
    :param factor: factor for the reference
    :type factor: numeric
    :param delta: delta for the reference
    :type delta: numeric
    :returns: no return value

    **example**

    .. math::
        \dot{m} = \dot{m}_\mathrm{ref} \cdot factor + delta\\
        m_{ref}: \text{mass flow of referenced connection}

    """
    def __init__(self, ref_obj, factor, delta):
        if not isinstance(ref_obj, connection):
            msg = 'First parameter must be object of type connection.'
            raise TypeError(msg)

        if not (isinstance(factor, int) or isinstance(factor, float)):
            msg = 'Second parameter must be of type int or float.'
            raise TypeError(msg)

        if not (isinstance(delta, int) or isinstance(delta, float)):
            msg = 'Thrid parameter must be of type int or float.'
            raise TypeError(msg)

        self.obj = ref_obj
        self.f = factor
        self.d = delta

    def get_attr(self, key):
        """
        get the value of a ref attribute

        :param key: attribute to return its value
        :type key: str
        :returns:
            - :code:`self.__dict__[key]` if object has attribute key
            - :code:`None` if object has no attribute key
        """
        if key in self.__dict__:
            return self.__dict__[key]
        else:
            print(self.bus(), ' has no attribute \"', key, '\"')
            return None
