import frappe

frappe.utils.logger.set_log_level("INFO")

logger = frappe.logger('cbk_exchange_rate')

def info(message):
    logger.info(message)

def debug(message):
    logger.debug(message)

def warning(message):
    logger.warning(message)

def error(message):
    logger.error(message)

