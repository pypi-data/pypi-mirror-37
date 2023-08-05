# pylint: disable=C0122,C0103
import json
import pureyaml
import copy
from six import string_types

def deepupdate(original, update):
    """ recursively fill in missing elements
    of dictionary <update> according to defaults in
    <original>.

    Function uses copy.deepcopy() to avoid inadvertently
    copying references. Everything is copied by value.
    """
    for key, value in original.items():
        if key not in update:
            update[key] = copy.deepcopy(value)
        elif isinstance(value, dict):
            deepupdate(copy.deepcopy(value), update[key])

####################################
#    CHANNEL NAMESPACES
####################################
class Namespace(object):
    """
        This class accepts any dictionary and creates
        a new object that can be traversed via the
        '.' (dot) operator instead of normal dictionary
        syntax (e.g. d['key'], d.get('key')).

        Example:

            >>> d = {'a':{'b':{'c':'d'}}}
            >>> ns = Namespace(**d)
            >>> ns.a.b.c
            d

        There are also methods to assist in dumping
        the new namespace to JSON and YAML formats.
    """
    def __init__(self, **kw):
        # TODO: basically, the leaf() function, takes a dict and then
        # makes a NS out of it. so, if self.__dict__ gets updated,
        # you could just call leaf() on it again. a merge() function
        # would, then, just merge the two dicts, then run through
        # the result with leaf - updating (merging) the two NS's.
        self.leaf(self, kw)

    def __iter__(self):
        for k, v in self.__dict__.items():
            if isinstance(v, Namespace):
                v = dict(v)
            yield k, v


    @classmethod
    def leaf(cls, ns, d):
        for k, v  in d.items():
            try:
                t = json.loads(json.dumps(v))
                if isinstance(t, dict):
                    v = t
            except (TypeError, ValueError):
                pass
            if isinstance(d.get(k), dict):
                if k == 'app_specific_config':
                    ns.__dict__[k] = v
                    continue
                leaf_ns = Namespace(**v)
                setattr(ns, k, leaf_ns)
                ns.__dict__[k] = leaf_ns
                cls.leaf(leaf_ns, v)
            else:
                setattr(ns, k, v)
                ns.__dict__[k] = v

    def to_yaml(self):
        return pureyaml.dumps(dict(self), sort_keys=True, allow_unicode=True)

    def to_json(self, indent=0):
        return json.dumps(dict(self), indent=indent)


class ChannelNamespace(Namespace):
    """
        This class has all of the benefits of the
        Namespace class, but it fills any missing
        elements so that the edged Channel object
        can use the '.' operator in source code
        safely.
    """
    def __init__(self, **kw):
        if not kw.get('__ns_no_defaults__'):
            # assure we have a basic namespace
            deepupdate(BASIC_CHANNEL_SCHEMA_DEFAULTS, kw)
            # this key has the bare minimum for any fieldbus-type in exosense
            if kw['protocol_config'].get('application'):
                if 'Modbus_TCP' == kw['protocol_config'].get('application'):
                    deepupdate(MODBUS_TCP_CHANNEL_SCHEMA_DEFAULTS, kw)
                elif 'Modbus_RTU' == kw['protocol_config'].get('application'):
                    deepupdate(MODBUS_RTU_CHANNEL_SCHEMA_DEFAULTS, kw)
                else:
                    deepupdate(CLASSIC_CHANNEL_SCHEMA_DEFAULTS, kw)
        Namespace.__init__(self, **kw)


####################################
#    CHANNEL SCHEMAS
####################################

BASIC_CHANNEL_SCHEMA_TYPE_MAP = {
    "display_name": str,
    "description": str,
    "properties": {
        "data_type": str,
        "data_unit": str,
        "min": float,
        "max": float,
        "precision": float,
        "value_mapping": str,
        "device_diagnostic": bool,
    },
    "protocol_config": {
        "application": str,
        "interface": str,
        "input_raw": {
            "max": float,
            "min": float,
            "unit": str,
        },
        "multiplier": float,
        "offset": float,
        "sample_rate": float,
        "report_rate": float,
        "report_on_change": bool,
        "down_sample": str,
        "app_specific_config": {},
    }
}

BASIC_CHANNEL_SCHEMA_DEFAULTS = {
    "display_name": "not specified",
    "description": "not specified",
    "properties": {
        "data_type": "not specified",
    },
    "protocol_config": {
        "application": "not specified",
        "interface": "not specified",
        "multiplier": 1,
        "offset": 0,
        "sample_rate": 1000,
        "report_rate": 1000,
        "report_on_change": False,
        "down_sample": "ACT",
        "app_specific_config": {},
    }
}

CLASSIC_CHANNEL_SCHEMA_TYPE_MAP = {
    "protocol_config": {
        "app_specific_config": {
            "module": str,
            "function": str,
            "parameters": dict,
            "positionals": list,
        }
    }
}
CLASSIC_CHANNEL_SCHEMA_DEFAULTS = {
    "protocol_config": {
        "app_specific_config": {
            "module": "time",
            "function": "time",
            "parameters": {},
            "positionals": [],
        }
    }
}
deepupdate(
    BASIC_CHANNEL_SCHEMA_DEFAULTS,
    CLASSIC_CHANNEL_SCHEMA_DEFAULTS
)


####################################
#    MODBUS TCP CHANNEL SCHEMA
####################################

MODBUS_TCP_CHANNEL_SCHEMA_TYPE_MAP = {
    "protocol_config": {
        "application": str,
        "interface": str,
        "app_specific_config": {
            "ip_address": str,
            "port": int,
            "register_range": str,
            "register_offset": int,
            "register_count":  int,
            "byte_endianness": str,
            "register_endianness": str,
            "evaluation_mode": str,
            "bitmask": hex,
        },
    }
}

MODBUS_TCP_CHANNEL_SCHEMA_DEFAULTS = {
    "protocol_config": {
        "app_specific_config": {
            "ip_address": "127.0.0.1",
            "port": 5020,
            "register_range": "INPUT_COIL",
            "register_offset": 0,
            "register_count":  1,
            "byte_endianness": "not specified",
            "register_endianness": "not specified",
            "evaluation_mode": "not specified",
            "bitmask": 0xFFFF,
        },
    }
}
deepupdate(
    BASIC_CHANNEL_SCHEMA_DEFAULTS,
    MODBUS_TCP_CHANNEL_SCHEMA_DEFAULTS
)
####################################
#    MODBUS RTU CHANNEL SCHEMA
####################################

MODBUS_RTU_CHANNEL_SCHEMA_TYPE_MAP = {
    "protocol_config": {
        "app_specific_config": {
            "slave_id": int,
            "register_range": str,
            "register_offset": int,
            "register_count":  int,
            "byte_endianness": str,
            "register_endianness": str,
            "evaluation_mode": str,
            "bitmask": hex,
        },
    }
}

MODBUS_RTU_CHANNEL_SCHEMA_DEFAULTS = {
    "protocol_config": {
        "app_specific_config": {
            "slave_id": 1,
            "register_range": "not specified",
            "register_offset": None,
            "register_count":  None,
            "byte_endianness": "not specified",
            "register_endianness": "not specified",
            "evaluation_mode": "not specified",
            "bitmask": 0xFFFF,
        },
    },
    "config_application": {
        "application_display_name" : "Modbus RTU",
        "interfaces" : [
            {
                "interface" : "/dev/ttyUSB1",
                "baud_rate" :  19200,
                "stop_bits" : 0,
                "parity" : 'N'
            }
        ],
    }
}
deepupdate(
    BASIC_CHANNEL_SCHEMA_DEFAULTS,
    MODBUS_RTU_CHANNEL_SCHEMA_DEFAULTS
)

