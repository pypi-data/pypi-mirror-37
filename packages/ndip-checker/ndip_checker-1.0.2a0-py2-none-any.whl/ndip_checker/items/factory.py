# encoding: utf-8
from utils import command_confirm
from . import BingChengJiLuItem, TuPianItem, PeiYangItem


def generate_peiyang(*args):
    return PeiYangItem(*args)


def generate_tupian(*args):
    return TuPianItem(*args)


def generate_bjcl(*args):
    return BingChengJiLuItem(*args)


ITEMS = {u'培养': generate_peiyang, u'涂片': generate_tupian, u'病程记录': generate_bjcl}


def check(item, patient_name, expected_date, fix=False):
    """ Check items are valid, and fix it.

    :returns
    True: if fixed are done
    False: no fix did
    """
    fixed = False   # tag for whether checks fixed

    if item['item'] in ITEMS.keys() and 'data' in item:
        obj = ITEMS[item['item']](item, patient_name, expected_date)
        if not obj.is_valid():
            if fix and command_confirm():
                fixed = True
                obj.update()

    return fixed
