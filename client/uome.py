from collections import namedtuple

UOMe = namedtuple("UOMe", "group user borrower value description "
                          "signature  uuid")


def from_list(uome_list):
    """ Converts a UOMe in list format into an UOMe object """
    return UOMe(*uome_list)
