# This Python file uses the following encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import object
import dpaycli as stm


class SharedInstance(object):
    """Singelton for the DPay Instance"""
    instance = None
    config = {}


def shared_dpay_instance():
    """ This method will initialize ``SharedInstance.instance`` and return it.
        The purpose of this method is to have offer single default
        dpay instance that can be reused by multiple classes.

        .. code-block:: python

            from dpaycli.account import Account
            from dpaycli.instance import shared_dpay_instance

            account = Account("test")
            # is equivalent with
            account = Account("test", dpay_instance=shared_dpay_instance())

    """
    if not SharedInstance.instance:
        clear_cache()
        SharedInstance.instance = stm.DPay(**SharedInstance.config)
    return SharedInstance.instance


def set_shared_dpay_instance(dpay_instance):
    """ This method allows us to override default dpay instance for all users of
        ``SharedInstance.instance``.

        :param dpaycli.dpay.DPay dpay_instance: DPay instance
    """
    clear_cache()
    SharedInstance.instance = dpay_instance


def clear_cache():
    """ Clear Caches
    """
    from .blockchainobject import BlockchainObject
    BlockchainObject.clear_cache()


def set_shared_config(config):
    """ This allows to set a config that will be used when calling
        ``shared_dpay_instance`` and allows to define the configuration
        without requiring to actually create an instance
    """
    if not isinstance(config, dict):
        raise AssertionError()
    SharedInstance.config.update(config)
    # if one is already set, delete
    if SharedInstance.instance:
        clear_cache()
        SharedInstance.instance = None
