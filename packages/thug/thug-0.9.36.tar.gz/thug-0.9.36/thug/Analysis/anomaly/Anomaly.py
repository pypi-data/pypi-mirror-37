import logging

log = logging.getLogger("Thug")


from .AnomalyChecks import ELEMENT_ALERTS
from .AnomalyChecks import ELEMENT_CHECKLIST


class Anomaly(object):
    def __init__(self):
        pass

    def __getattr__(self, key):
        if key.startswith('check_element_out_of_'):
            tag = key.split('check_element_out_of_')[1]
            return lambda check: self.check_element_out_of_tag(tag, check)

        if key.startswith('check_element_in_'):
            tag = key.split('check_element_in_')[1]
            return lambda check: self.check_element_in_tag(tag, check)

        raise AttributeError

    def collect_element_parents(self, element):
        parents = list()

        p = getattr(element, 'parents', None)
        if p is None:
            return parents

        for item in p:
            n = getattr(item, 'name', None)
            if n:
                parents.append(n)

        return parents

    def check_element_out_of_tag(self, tag, check):
        if tag not in check['parents']:
            msg = ELEMENT_ALERTS['OUT_OF_HTML'].format(check['element_name'],
                                                       check['type_'],
                                                       ', '.join(check['threats']))
            log.warning(msg)

    def check_element_in_tag(self, tag, check):
        if tag in check['parents']:
            msg = ELEMENT_ALERTS['IN_HEAD'].format(check['element_name'],
                                                   check['type_'],
                                                   ', '.join(check['threats']))
            log.warning(msg)

    def check_element(self, element, type_ = ""):
        element_name = getattr(element, 'name', None)
        if element_name is None:
            return

        parents = self.collect_element_parents(element)

        for method_name, threats in ELEMENT_CHECKLIST[element_name]:
            method = getattr(self, method_name, None)
            if method is None:
                continue

            check = {
                'element_name' : element_name,
                'element'      : element,
                'parents'      : parents,
                'type_'        : type_,
                'threats'      : threats
            }

            method(check)
