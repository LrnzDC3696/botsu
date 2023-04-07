DURATION_UNITS = ('days', 'hours', 'minutes', 'seconds')


def iter_deconstruct_duration(duration):
    """
    Deconstructs the duration into days, hours, minutes, seconds.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    duration : `TimeDelta`
        The duration to deconstruct.
    
    Yields
    ------
    unit : `int`
    """
    yield duration.days
    hours, seconds = divmod(duration.seconds, 60 * 60)
    yield hours
    yield from divmod(seconds, 60)


def build_duration_string(duration):
    """
    Converts the mute duration to string.
    
    Parameters
    ----------
    duration : `TimeDelta`
        Mute duration.
    
    Returns
    -------
    duration_string : `str`
    """
    string_parts = []
    
    field_added = False
    
    for unit_value, unit_name in zip(iter_deconstruct_duration(duration), DURATION_UNITS):
        if unit_value:
            if field_added:
                string_parts.append(', ')
            else:
                field_added = True
            
            string_parts.append(str(unit_value))
            string_parts.append(' ')
            string_parts.append(unit_name)
    
    return ''.join(string_parts)
