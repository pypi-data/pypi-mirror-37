#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# : Corpus Module
# Author:
# c(Developer) ->     {'Egor Savin'}
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

###Programm Info######

 
import platform
from raven import Client
from raven.processors import SanitizePasswordsProcessor
from zas_rep_tools.src.utils.debugger import p

#self.client.captureException()
#Raven.setExtraContext({
#    arbitrary: {key: value},
#    foo: "bar"
#});

#https://github.com/getsentry/raven-python/blob/master/docs/api.rst

def initialisation():

    #SanitizePasswordsProcessor.KEYS =  frozenset(['sentry_dsn', 'password', 'passwd', 'access_token', 'secret', 'apikey', 'api_key', 'authorization', 'consumer_key', 'consumer_secret', 'access_token', 'access_token_secret'])
    #p(SanitizePasswordsProcessor.KEYS)
    platform_info = {"platform":platform.platform(), "uname":platform.uname(), "system":platform.system(), "processor":platform.processor(), "machine":platform.machine(), "version":platform.version(), "architecture":platform.architecture  }
    python_info = {"python_build":platform.python_build(), "python_compiler":platform.python_compiler(),  "python_implementation":platform.python_implementation(), "python_version":platform.python_version(), }
    user_info = {"platform_info":platform_info, "python_info":python_info}
    #p(user_info)
    client = Client(dsn='https://0ec650403a06441aa6075e14322a9b15:ba5a980db0064f25b118d724eeb4d877@sentry.io/1213596',
            auto_log_stacks=True,
            include_paths=[__name__.split('.', 1)[0]],
            release = '0.1',
            #user = user_info,
            #intern_attribute = self.__dict__,
            ignore_exceptions = [
            'Http404'
            ],
            processors = (
            'raven.processors.SanitizePasswordsProcessor',
            ),
            sanitize_keys = ['_consumer_key', '_consumer_secret', '_access_token', '_access_token_secret'],
            # pass along the version of your application
            # release='1.0.0'
            # release=raven.fetch_package_version('my-app')
            #release=raven.fetch_git_sha(os.path.dirname(__file__)),
            )
    #p(client.sanitize_keys)
    client.module_cache['raven.processors.SanitizePasswordsProcessor'].KEYS = frozenset(['sentry_dsn', 'password', 'passwd', 'access_token', 'secret', 'apikey', 'api_key', 'authorization', '_consumer_key', '_consumer_secret', '_access_token', '_access_token_secret'])
    #p(client.module_cache['raven.processors.SanitizePasswordsProcessor'].KEYS)
    client.context.merge({'user': user_info})
    #client.context.merge({'user': python_info})
    #client.context.merge({'user': platform_info})


    return client