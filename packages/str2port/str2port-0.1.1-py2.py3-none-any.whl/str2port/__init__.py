from .core import StrToPort


def str2port(s, use_iana=False):
    return StrToPort(s, use_iana=use_iana).all()
