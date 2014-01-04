def individual(elements):
    return [e.segment() for e in elements]

def timeInstantOverlapping(elements):
    """
    agregate into one segment the elements that overlap in the same instant of time
    """
    pass


def trainOverlapping(elements,ms_of_separation=1):
    """
    agregate into the same segment the elements that are separate less than ms_of_separation time
    """
    pass


