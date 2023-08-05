#coding=utf8

# name = 'multiprocessing_log_manager'
__all__ = ['LogManager','simple_logger']
from .log_manager import LogManager
simple_logger = LogManager('simple').get_logger_and_add_handlers()