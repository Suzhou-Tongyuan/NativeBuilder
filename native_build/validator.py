def validate(typ: type, instance: Any) -> bool:
    for property_name, property_type in typ.__annotations__.items():
        value = instance.get(property_name, None)
        if value is None:
            # Check for missing keys
            print(f"Missing key: {property_name}")
            return False
        elif property_type not in (int, float, bool, str):
            # check if property_type is object (e.g. not a primitive)
            result = validate(property_type, value)
            if result is False:
                return False
        elif not isinstance(value, property_type):
            # Check for type equality
            print(f"Wrong type: {property_name}. Expected {property_type}, got {type(value)}")
            return False
    return True