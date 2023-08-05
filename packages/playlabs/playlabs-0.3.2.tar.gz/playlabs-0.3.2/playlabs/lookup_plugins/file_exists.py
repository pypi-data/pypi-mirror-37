import os

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        for term in terms:
            display.vv("File lookup term: %s" % term)
            if not os.path.exists(term):
                raise AnsibleError("could locate file in lookup: %s" % term)
        return True
