
verbose_formatter = {
    'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'}

file_handler = {
    'level': 'DEBUG',
    'class': 'logging.FileHandler',
    'filename': None,
    'formatter': 'verbose'
}
