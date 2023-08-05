KEY_ID = 'identification'
KEY_FIX_INFO = 'fix_info'
KEY_FINISH_TAG = 'is_finished'
KEY_CLASS_STATUS = 'class'


from .base import BaseItem
from .bingchengjilu import BingChengJiLuItem
from .tupian import TuPianItem
from .peiyang import PeiYangItem
from .factory import ITEMS, check

from .utils import command_confirm