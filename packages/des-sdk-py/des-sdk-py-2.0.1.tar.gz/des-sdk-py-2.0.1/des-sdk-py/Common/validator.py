from Common import exceptions
import logging
log = logging.getLogger(__name__)
#TODO detect whether the params are valid
def validate(input, params):
    log.debug("detect whether the input is valid.")
    for key, value in input.items():
        pType = type(value)
        if value.get('required') and not params.get(key):
            log.error("invalid parameter: %s must be non-nil" % key)
            return False
        if not params.get(key):
            continue

        valueType = value.get("type")
        if "string" == valueType:
            if type(params.get(key)) == "str":
                continue
        elif "integer" == valueType:
            if type(params.get(key)) == "int":
                continue
        elif "boolean" == valueType:
            if type(params.get(key)) == "bool":
                continue
        elif "long" == valueType:
            if type(params.get(key)) == "int":
                continue
        elif "float" == valueType:
            if type(params.get(key)) == "float":
                continue
        elif "double" == valueType:
            if type(params.get(key)) == "float":
                continue
        elif "date" == valueType:
            if type(params.get(key)) == "str":
                continue
        else:
            raise exceptions.InvalidTxParamsException("invalid input params type")
    return True

