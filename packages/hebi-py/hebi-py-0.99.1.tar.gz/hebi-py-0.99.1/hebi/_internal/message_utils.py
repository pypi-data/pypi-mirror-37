# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  HEBI Core python API - Copyright 2018 HEBI Robotics
#  See https://hebi.us/softwarelicense for license details
#
# -----------------------------------------------------------------------------


import math
import numpy
from ctypes import (byref, create_string_buffer,
                    c_int, c_int32, c_int64, c_uint8,
                    c_uint64, c_float, c_double)
from functools import partial as funpart

from .graphics import Color, color_from_int, string_to_color
from .raw import *
from .utils import WeakReferenceContainer
from . import type_utils
from .type_utils import decode_string_buffer as decode_str
from .type_utils import create_string_buffer_compat as create_str

# -----------------------------------------------------------------------------
# Debug Field Containers
# -----------------------------------------------------------------------------


class GroupNumberedFloatFieldContainer(WeakReferenceContainer):
  """
  TODO: Document
  """

  def __throw_badattr(self, val):
    raise AttributeError('Numbered float field object has no attribute'
                         ' \'{0}\''.format(val))

  def _parse_attr(self, val):
    """
    Looks for 'float' at beginning, and if it finds this, we will attempt
    to parse an integer after this string
    """

    if not val.startswith('float'):
      return None
    try:
      number = int(val[5:])
      if number < 1 or number > self._count:
        self.__throw_badattr(val)
      return number
    except:
      self.__throw_badattr(val)

  def __call_get_numbered_float(self, number):
    internal = self._get_ref()
    tmp = c_float(0.0)
    self.__get_numbered_float(internal, self._field, number, byref(tmp))
    return tmp.value

  def __getattr__(self, val):
    number = self._parse_attr(val)
    if number:
      return self.__call_get_numbered_float(number)
    return super(GroupNumberedFloatFieldContainer, self).__getattr__(val)

  def __setattr__(self, name, val):
    """
    By default, this is _not_ mutable.
    Use the mutable subclass for mutability.
    """
    number = self._parse_attr(name)
    if number:
      raise AttributeError('Numbered float field {0}'.format(number) +
                           ' is not mutable')
    else:
      return super(GroupNumberedFloatFieldContainer, self).__setattr__(name, val)

  def __find_functions(self, message_str):
    from . import raw
    self.__get_numbered_float =\
      getattr(raw, 'hebi{0}GetNumberedFloat'.format(message_str))

  def __init__(self, internal, message_str, field, count):
    if count < 1:
      raise ValueError('count must be greater than zero')
    super(GroupNumberedFloatFieldContainer, self).__init__(internal)
    self._field = field
    self._count = count
    self.__find_functions(message_str)

  @property
  def count(self):
    return self._count

  @property
  def fields(self):
    ret = ['float']*self._count
    for i, entry in enumerate(ret):
      ret[i] = entry + str(i + 1)
    return ret


class MutableGroupNumberedFloatFieldContainer(GroupNumberedFloatFieldContainer):
  """
  TODO: Document
  """

  def __call_set_numbered_float(self, number, value):
    try:
      value = float(value)
    except:
      raise ValueError('Cannot set numbered float field {0}'.format(number) +
                       ' to value {0}'.format(value))

    internal = self._get_ref()
    tmp = c_float(value)
    self.__set_numbered_float(internal, self._field, number, byref(tmp))


  def __setattr__(self, name, val):
    number = self._parse_attr(name)
    if number:
      self.__call_set_numbered_float(number, val)
    else:
      return super(MutableGroupNumberedFloatFieldContainer, self).__setattr__(name, val)

  def __find_functions(self, message_str):
    from . import raw
    self.__set_numbered_float =\
      getattr(raw, 'hebi{0}SetNumberedFloat'.format(message_str))

  def __init__(self, internal, message_str, field, count):
    super(MutableGroupNumberedFloatFieldContainer,
          self).__init__(internal, message_str, field, count)

    self.__find_functions(message_str)


# -----------------------------------------------------------------------------
# IoField classes
# -----------------------------------------------------------------------------


class GroupMessageIoFieldBankContainer(WeakReferenceContainer):
  """
  TODO: Document
  """

  __slots__ = ['_bank']

  def has_int(self, pin_number):
    container = self._get_ref()
    return container.has_int(self._bank, pin_number)

  def has_float(self, pin_number):
    container = self._get_ref()
    return container.has_float(self._bank, pin_number)

  def get_int(self, pin_number):
    container = self._get_ref()
    return container.get_int(self._bank, pin_number)

  def get_float(self, pin_number):
    container = self._get_ref()
    return container.get_float(self._bank, pin_number)

  def __init__(self, bank, io_field_container):
    super(GroupMessageIoFieldBankContainer, self).__init__(io_field_container)
    self._bank = bank

    if io_field_container._mutable:
      def set_int(pin_number, value):
        container = self._get_ref()
        container.set_int(self._bank, pin_number, value)

      def set_float(pin_number, value):
        container = self._get_ref()
        container.set_float(self._bank, pin_number, value)

      setattr(self, 'set_int', set_int)
      setattr(self, 'set_float', set_float)


class GroupMessageIoFieldContainer(WeakReferenceContainer):
  """
  TODO: Document
  """

  __slots__ = ['_a', '_b', '_c', '_d', '_e', '_f', '_mutable', '__get_float', '__get_int', '_set_float', '_set_int',
               '__weakref__']

  def __initialize(self, message_str):
    from . import raw
    self.__get_int = getattr(raw, 'hebi{0}GetIoPinInt'.format(message_str))
    self.__get_float = getattr(raw, 'hebi{0}GetIoPinFloat'.format(message_str))

    # Group Message type is mutable -- add setters
    if self._mutable:
      c_set_int = getattr(raw, 'hebi{0}SetIoPinInt'.format(message_str))
      c_set_float = getattr(raw, 'hebi{0}SetIoPinFloat'.format(message_str))

      def seti(bank, pin_number, value):
        group_message = self._get_ref()
        pin_number = c_size_t(pin_number)
        value = __do_broadcast(group_message, bank, value, numpy.int64)
        tmp = c_int64(0)
        for i, message in enumerate(group_message.modules):
          tmp.value = value[i]
          c_set_int(message, bank, pin_number, byref(tmp))


      def setf(bank, pin_number, value):
        group_message = self._get_ref()
        pin_number = c_size_t(pin_number)
        value = __do_broadcast(group_message, bank, value, numpy.float32)
        tmp = c_float(0.0)
        for i, message in enumerate(group_message.modules):
          tmp.value = value[i]
          c_set_float(message, bank, pin_number, byref(tmp))


      self._set_int = seti
      self._set_float = setf


    bank_a = getattr(raw, '{0}IoBankA'.format(message_str))
    bank_b = getattr(raw, '{0}IoBankB'.format(message_str))
    bank_c = getattr(raw, '{0}IoBankC'.format(message_str))
    bank_d = getattr(raw, '{0}IoBankD'.format(message_str))
    bank_e = getattr(raw, '{0}IoBankE'.format(message_str))
    bank_f = getattr(raw, '{0}IoBankF'.format(message_str))

    self._a = GroupMessageIoFieldBankContainer(bank_a, self)
    self._b = GroupMessageIoFieldBankContainer(bank_b, self)
    self._c = GroupMessageIoFieldBankContainer(bank_c, self)
    self._d = GroupMessageIoFieldBankContainer(bank_d, self)
    self._e = GroupMessageIoFieldBankContainer(bank_e, self)
    self._f = GroupMessageIoFieldBankContainer(bank_f, self)

  def __init__(self, group_message, message_str, mutable=False):
    super(GroupMessageIoFieldContainer, self).__init__(group_message)
    self._mutable = mutable
    self.__initialize(message_str)

  def has_int(self, bank, pin_number):
    group_message = self._get_ref()
    ret = numpy.empty(group_message.size, bool)
    pin_number = c_size_t(pin_number)

    for i, message in enumerate(group_message.modules):
      ret[i] = self.__get_int(message, bank, pin_number, None) == StatusSuccess
    return ret

  def has_float(self, bank, pin_number):
    group_message = self._get_ref()
    ret = numpy.empty(group_message.size, bool)
    pin_number = c_size_t(pin_number)

    for i, message in enumerate(group_message.modules):
      ret[i] = self.__get_float(message, bank, pin_number, None) == StatusSuccess
    return ret

  def get_int(self, bank, pin_number):
    group_message = self._get_ref()
    ret = numpy.empty(group_message.size, numpy.int64)
    pin_number = c_size_t(pin_number)
    tmp = c_int64(0)

    for i, message in enumerate(group_message.modules):
      if self.__get_int(message, bank, pin_number, byref(tmp)) != StatusSuccess:
        ret[i] = 0
      else:
        ret[i] = tmp.value
    return ret

  def get_float(self, bank, pin_number):
    group_message = self._get_ref()
    ret = numpy.empty(group_message.size, numpy.float32)
    pin_number = c_size_t(pin_number)
    tmp = c_float(0.0)

    for i, message in enumerate(group_message.modules):
      if self.__get_float(message, bank, pin_number, byref(tmp)) != StatusSuccess:
        ret[i] = numpy.nan
      else:
        ret[i] = tmp.value
    return ret

  @property
  def a(self):
    return self._a

  @property
  def b(self):
    return self._b

  @property
  def c(self):
    return self._c

  @property
  def d(self):
    return self._d

  @property
  def e(self):
    return self._e

  @property
  def f(self):
    return self._f


# -----------------------------------------------------------------------------
# LED Field Containers
# -----------------------------------------------------------------------------

class GroupMessageLEDFieldContainer(WeakReferenceContainer):

  def __call_get_led_color(self):
    group_message = self._get_ref()
    r = c_uint8(0)
    g = c_uint8(0)
    b = c_uint8(0)
    ret = [Color(0, 0, 0)] * group_message.size

    for i, message in enumerate(group_message.modules):
      if (self.__get_led_color(message, self._field, byref(r), byref(g), byref(b)) != StatusSuccess):
        # TODO: handle error
        pass
      color = ret[i]
      color.r = r.value
      color.g = g.value
      color.b = b.value
      ret[i] = color

    return ret

  def __find_functions(self, message_str):
    from . import raw
    self.__get_led_color = getattr(raw, 'hebi{0}GetLedColor'.format(message_str))

  def __init__(self, internal, message_str, field):
    super(GroupMessageLEDFieldContainer, self).__init__(internal)
    self.__find_functions(message_str)
    self._field = field

  @property
  def color(self):
    return self.__call_get_led_color()


class MutableGroupMessageLEDFieldContainer(GroupMessageLEDFieldContainer):
  __slots__ = ['__has_led_module_control', '__set_led_override_color', '__set_led_module_control', '__clear_led']

  def _clear_all_leds(self):
    group_message = self._get_ref()
    for i, message in enumerate(group_message.modules):
      self.__clear_led(message, self._field)

  def _clear_led(self, index):
    message = self._get_ref().modules[index]
    self.__clear_led(message, self._field)

  def _set_all_led_module_controls(self):
    group_message = self._get_ref()
    for i, message in enumerate(group_message.modules):
      self.__set_led_module_control(message, self._field)

  def _set_led_module_control(self, index):
    message = self._get_ref().modules[index]
    self.__set_led_module_control(message, self._field)

  def _get_has_led_module_control(self, index):
    message = self._get_ref().modules[index]
    return bool(self.__has_led_module_control(message, self._field))

  def _set_led_color(self, index, color):
    message = self._get_ref().modules[index]
    r = c_uint8(color.r)
    g = c_uint8(color.g)
    b = c_uint8(color.b)
    self.__set_led_override_color(message, self._field, r, g, b)

  def __set_colors(self, colors):
    if colors is None:
      self._clear_all_leds()
      return
    elif type(colors) is str:
      colors = [string_to_color(colors)] * self._get_ref().size
    elif type(colors) is int:
      colors = [color_from_int(colors)] * self._get_ref().size
    elif isinstance(colors, Color):
      colors = [colors] * self._get_ref().size
    elif not (hasattr(colors, '__len__')):
      raise ValueError('Cannot broadcast input to array of colors')

    for i, color in enumerate(colors):
      if color is None:
        self._clear_led(i)
      elif color.a == 0:
        """ Let module have control of LED color """
        self.__set_led_module_control(i)
      elif color.a == 255:
        """ Set LED override color without alpha blending (opaque color) """
        self._set_led_color(i, color)
      else:
        """ Do alpha blending """
        # For now, just set led color without blending :(
        self._set_led_color(i, color)

  def __find_functions(self, message_str):
    from . import raw
    self.__has_led_module_control = getattr(raw, 'hebi{0}HasLedModuleControl'.format(message_str))
    self.__set_led_override_color = getattr(raw, 'hebi{0}SetLedOverrideColor'.format(message_str))
    self.__set_led_module_control = getattr(raw, 'hebi{0}SetLedModuleControl'.format(message_str))
    self.__clear_led = getattr(raw, 'hebi{0}ClearLed'.format(message_str))

  def __init__(self, internal, message_str, field):
    super(MutableGroupMessageLEDFieldContainer, self).__init__(internal, message_str, field)
    self.__find_functions(message_str)

  @property
  def color(self):
    return super(MutableGroupMessageLEDFieldContainer, self).color

  @color.setter
  def color(self, value):
    self.__set_colors(value)


# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------

def __check_broadcastable(group_type, field, value):
  if group_type.size > 1:
    if not field.allow_broadcast:
      raise ValueError('Cannot broadcast scalar value \'{0}\' '.format(value) +
                       'to the field \'{0}\' '.format(field.name) +
                       'in all modules of the group.' +
                       '\nReason: {0}'.format(field.not_broadcastable_reason))


def __do_broadcast(group_message, field, value, dtype):
  if hasattr(value, '__len__') and type(value) is not str:
    __assert_same_length(group_message, value)
    if dtype is str:
      return value
    else:
      return numpy.array(value, dtype=dtype)
  else: # Is scalar; each module in group will be set to this
    __check_broadcastable(group_message, field, value)
    return numpy.array([value] * group_message.size, dtype=dtype)


def __assert_same_length(group_message, b):
  if group_message.size != len(b):
    raise ValueError('Input array must have same size as number of modules in group message')


# -----------------------------------------------------------------------------
# Accessor Functions
# -----------------------------------------------------------------------------


import threading
class MessagesTLS(threading.local):

  __slots__ = ['c_int32', 'c_uint8', 'c_int64', 'c_uint64', 'c_size_t', 'c_float', 'c_vector3f', 'c_quaternionf',
               'c_null_str', 'c_str']

  def __init__(self):
    super(MessagesTLS, self).__init__()
    self.c_int32 = c_int32(0)
    self.c_uint8 = c_uint8(0)
    self.c_int64 = c_int64(0)
    self.c_uint64 = c_uint64(0)
    self.c_size_t = c_size_t(0)
    self.c_float = c_float(0)
    self.c_vector3f = type_utils.create_float_buffer(3)
    self.c_quaternionf = type_utils.create_float_buffer(4)
    self.c_null_str = c_char_p(None)
    self.c_str = create_str(512)


_tls = MessagesTLS()


def __get_flag(group_message, field, getter=None, output=None):
  if output is None:
    ret = numpy.empty(group_message.size, numpy.bool)
  else:
    ret = output
  for i, message in enumerate(group_message.modules):
    ret[i] = bool(getter(message, field))
  return ret


def __get_bool(group_message, field, getter=None, output=None):
  if output is None:
    ret = numpy.empty(group_message.size, numpy.bool)
  else:
    ret = output
  tmp = _tls.c_int32
  for i, message in enumerate(group_message.modules):
    if getter(message, field, byref(tmp)) != StatusSuccess:
      ret[i] = False
    else:
      ret[i] = bool(tmp.value)
  return ret


def __get_uint8(group_message, field, getter=None, output=None):
  if output is None:
    ret = numpy.empty(group_message.size, numpy.uint8)
  else:
    ret = output
  tmp = _tls.c_uint8
  for i, message in enumerate(group_message.modules):
    if getter(message, field, byref(tmp)) != StatusSuccess:
      ret[i] = 0
    else:
      ret[i] = tmp.value
  return ret


def __get_int32(group_message, field, getter=None, output=None):
  if output is None:
    ret = numpy.empty(group_message.size, numpy.int32)
  else:
    ret = output
  tmp = _tls.c_int32
  for i, message in enumerate(group_message.modules):
    if getter(message, field, byref(tmp)) != StatusSuccess:
      ret[i] = 0
    else:
      ret[i] = tmp.value
  return ret


def __get_uint64(group_message, field, getter=None, output=None):
  if output is None:
    ret = numpy.empty(group_message.size, numpy.uint64)
  else:
    ret = output
  tmp = _tls.c_uint64
  for i, message in enumerate(group_message.modules):
    if getter(message, field, byref(tmp)) != StatusSuccess:
      ret[i] = 0
    else:
      ret[i] = tmp.value
  return ret


def __get_float(group_message, field, getter=None, output=None):
  if output is None:
    ret = numpy.empty(group_message.size, numpy.float32)
  else:
    ret = output
  tmp = _tls.c_float
  for i, message in enumerate(group_message.modules):
    if getter(message, field, byref(tmp)) != StatusSuccess:
      ret[i] = numpy.nan
    else:
      ret[i] = tmp.value
  return ret


def __get_highresangle(group_message, field, getter=None, output=None):
  if output is None:
    ret = numpy.empty(group_message.size, numpy.float64)
  else:
    ret = output
  revolutions = _tls.c_int64
  radian_offset = _tls.c_float
  for i, message in enumerate(group_message.modules):
    if getter(message, field, byref(revolutions), byref(radian_offset)) != StatusSuccess:
      ret[i] = numpy.nan
    else:
      ret[i] = revolutions.value*two_pi + radian_offset.value
  return ret


def __get_vector_3f(group_message, field, getter=None, output=None):
  if output is None:
    ret = numpy.empty((group_message.size, 3), numpy.float64)
  else:
    ret = output
  ptr = _tls.c_vector3f
  for i, message in enumerate(group_message.modules):
    if getter(message, field, ptr) != StatusSuccess:
      ret[i, 0:3] = numpy.nan
    else:
      ret[i, 0:3] = ptr
  return ret


def __get_quaternionf(group_message, field, getter=None, output=None):
  if output is None:
    ret = numpy.empty((group_message.size, 4), numpy.float64)
  else:
    ret = output
  ptr = _tls.c_quaternionf
  for i, message in enumerate(group_message.modules):
    if getter(message, field, ptr) != StatusSuccess:
      ret[i, 0:4] = numpy.nan
    else:
      ret[i, 0:4] = ptr
  return ret


def __get_string(group_message, field, getter=None, output=None):
  alloc_size_c = _tls.c_size_t
  alloc_size = 0
  null_str = _tls.c_null_str

  for i, message in enumerate(group_message.modules):
    res = getter(message, field, null_str, byref(alloc_size_c))
    alloc_size = max(alloc_size, alloc_size_c.value + 1)

  if output is not None:
    ret = output
  else:
    ret = [None] * group_message.size

  if alloc_size > len(_tls.c_str):
    string_buffer = create_string_buffer(alloc_size)
  else:
    string_buffer = _tls.c_str

  for i, message in enumerate(group_message.modules):
    alloc_size_c.value = alloc_size
    if getter(message, field, string_buffer, byref(alloc_size_c)) == StatusSuccess:
      ret[i] = decode_str(string_buffer.value)
    else:
      ret[i] = None
  return ret


# -----------------------------------------------------------------------------
# Mutator Functions
# -----------------------------------------------------------------------------

nan = float('nan')
inv_half_pi = 0.5/math.pi
two_pi = 2.0*math.pi


def __set_flag(group_message, field, value, setter=None):
  value = __do_broadcast(group_message, field, value, numpy.bool)
  val = _tls.c_int32
  for i, message in enumerate(group_message.modules):
    val.value = int(value[i])
    setter(message, field, val)


def __set_bool(group_message, field, value, setter=None):
  value = __do_broadcast(group_message, field, value, numpy.bool)
  tmp = _tls.c_int32
  for i, message in enumerate(group_message.modules):
    tmp.value = value[i]
    setter(message, field, byref(tmp))


def __set_uint8(group_message, field, value, setter=None):
  value = __do_broadcast(group_message, field, value, numpy.uint8)
  tmp = _tls.c_uint8
  for i, message in enumerate(group_message.modules):
    tmp.value = value[i]
    setter(message, field, byref(tmp))


def __set_int32(group_message, field, value, setter=None):
  value = __do_broadcast(group_message, field, value, numpy.int32)
  tmp = _tls.c_int32
  for i, message in enumerate(group_message.modules):
    tmp.value = value[i]
    setter(message, field, byref(tmp))


def __set_uint64(group_message, field, value, setter=None):
  value = __do_broadcast(group_message, field, value, numpy.uint64)
  tmp = _tls.c_uint64
  for i, message in enumerate(group_message.modules):
    tmp.value = value[i]
    setter(message, field, byref(tmp))


def __set_float(group_message, field, value, setter=None):
  value = __do_broadcast(group_message, field, value, numpy.float32)
  tmp = _tls.c_float
  for i, message in enumerate(group_message.modules):
    tmp.value = value[i]
    setter(message, field, byref(tmp))


def __set_highresangle(group_message, field, value, setter=None):
  value = __do_broadcast(group_message, field, value, numpy.float64)
  revolutions = _tls.c_int64
  offset = _tls.c_float
  for i, message in enumerate(group_message.modules):
    radians = value[i]
    if math.isnan(radians):
      revolutions.value = 0
      offset.value = nan
    else:
      revolutions_raw = radians * inv_half_pi
      offset.value, rev_d = math.modf(revolutions_raw)
      revolutions.value = int(rev_d)
      offset.value = offset.value * two_pi
    setter(message, field, byref(revolutions), byref(offset))


def __set_string(group_message, field, value, setter=None):
  value = __do_broadcast(group_message, field, value, str)
  alloc_size_c = _tls.c_size_t

  for i, message in enumerate(group_message.modules):
    val = value[i]
    alloc_size = len(val) + 1
    # TODO: use tls string buffer and copy val into it instead
    string_buffer = type_utils.create_string_buffer_compat(val, size=alloc_size)
    alloc_size_c.value = alloc_size
    setter(message, field, string_buffer, byref(alloc_size_c))


# -----------------------------------------------------------------------------
# Command
# -----------------------------------------------------------------------------


get_group_command_flag = funpart(__get_flag, getter=hebiCommandGetFlag)
get_group_command_bool = funpart(__get_bool, getter=hebiCommandGetBool)
get_group_command_enum = funpart(__get_int32, getter=hebiCommandGetEnum)
get_group_command_float = funpart(__get_float, getter=hebiCommandGetFloat)
get_group_command_highresangle = funpart(__get_highresangle, getter=hebiCommandGetHighResAngle)
get_group_command_string = funpart(__get_string, getter=hebiCommandGetString)

set_group_command_flag = funpart(__set_flag, setter=hebiCommandSetFlag)
set_group_command_bool = funpart(__set_bool, setter=hebiCommandSetBool)
set_group_command_enum = funpart(__set_int32, setter=hebiCommandSetEnum)
set_group_command_float = funpart(__set_float, setter=hebiCommandSetFloat)
set_group_command_highresangle = funpart(__set_highresangle, setter=hebiCommandSetHighResAngle)
set_group_command_string = funpart(__set_string, setter=hebiCommandSetString)


# -----------------------------------------------------------------------------
# Feedback
# -----------------------------------------------------------------------------


get_group_feedback_vector3f = funpart(__get_vector_3f, getter=hebiFeedbackGetVector3f)
get_group_feedback_quaternionf = funpart(__get_quaternionf, getter=hebiFeedbackGetQuaternionf)
get_group_feedback_uint64 = funpart(__get_uint64, getter=hebiFeedbackGetUInt64)
get_group_feedback_enum = funpart(__get_int32, getter=hebiFeedbackGetEnum)
get_group_feedback_float = funpart(__get_float, getter=hebiFeedbackGetFloat)
get_group_feedback_highresangle = funpart(__get_highresangle, getter=hebiFeedbackGetHighResAngle)


# -----------------------------------------------------------------------------
# Info
# -----------------------------------------------------------------------------


get_group_info_flag = funpart(__get_flag, getter=hebiInfoGetFlag)
get_group_info_enum = funpart(__get_int32, getter=hebiInfoGetEnum)
get_group_info_bool = funpart(__get_bool, getter=hebiInfoGetBool)
get_group_info_float = funpart(__get_float, getter=hebiInfoGetFloat)
get_group_info_highresangle = funpart(__get_highresangle, getter=hebiInfoGetHighResAngle)
get_group_info_string = funpart(__get_string, getter=hebiInfoGetString)


# -----------------------------------------------------------------------------
# Parsers
# -----------------------------------------------------------------------------


def __map_input_setter_delegate(group_message, values, setter, setter_field):
  mapped_values = [None] * group_message.size
  str_map = setter_field.substrates

  try:
    if type(values) is str:
      val = str_map[values.lower()]
      for i in range(0, group_message.size):
        mapped_values[i] = val
    else:
      for i, entry in enumerate(values):
        mapped_values[i] = str_map[entry.lower()]
  except KeyError as key:
    print('{0} is not a valid string parameter.'.format(key))
    print('Valid string parameters: {0}'.format("'" + "', '".join(setter_field.substrates.keys()) + "'"))
    raise
  setter(group_message, setter_field, mapped_values)


def setter_input_parser_delegate(group_message, values, setter, setter_field):
  """
  Maps strings (case insensitive) to a non-string type.
  Only used for fields which are not of type string

  This function assumes that `setter_field` has an attribute called `substrates`
  which returns a dictionary with :type str: keys and values of the type which
  the function `setter` expects
  """
  if not hasattr(setter_field, 'substrates'):
    raise RuntimeError('Field {0} has no substrates map field'.format(setter_field))
  if hasattr(values, '__len__') and type(values) is not str:  # Is "array-like" according to numpy
    for entry in values:
      if type(entry) is not str:
        # By default, delegate to regular `setter` routine
        setter(group_message, setter_field, values)
        return
    __map_input_setter_delegate(group_message, values, setter, setter_field)
  elif type(values) == str:
    __map_input_setter_delegate(group_message, values, setter, setter_field)
  else:
    setter(group_message, setter_field, values)
