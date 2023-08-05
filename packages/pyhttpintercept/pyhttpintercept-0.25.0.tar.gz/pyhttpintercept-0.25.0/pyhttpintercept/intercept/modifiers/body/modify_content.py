# encoding: utf-8

import logging_helper
from future.utils import iteritems
from pyhttpintercept.intercept.handlers.support import parse_dictionary_parameters

logging = logging_helper.setup_logging()


def modify(request,
           response,
           modifier,
           **_):

    if modifier.passes_filter(value=request,
                              wildcards=u''):

        # Set up parameters
        parse_dictionary_parameters(modifier)

        content = response.content

        for key, value in iteritems(modifier.params):
            try:
                logging.info(u'Modifing body content: Replacing {k} with {v}'.format(k=key,
                                                                                     v=value))
                content.replace(key, value)

            except Exception as err:
                logging.error(u'Failed to replace {k} with {v}: {err}'.format(k=key,
                                                                              v=value,
                                                                              err=err))

        response._content = content

    return response
