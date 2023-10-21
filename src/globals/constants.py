from globals.interfaces import Immutable

class CONSTANTS(Immutable):
    class FilesFoldersNames(Immutable):
        results = 'results'
        snapshot = 'snapshots'
        row_null_distribution_snapshot='row-null-distribution-snapshot'
        column_null_count_snapshot='column-null-count-snapshot'
        column_pair_null_pattern_snapshot='column-pair-null-pattern-snapshot'
        log_filename = 'data-quality-tools.log'
    class Logger(Immutable):
        class Formatters(Immutable):
            basic_log_formatter = {
                    "format": "[%(asctime)s] [%(levelname)8s] --> (%(name)s) - \"%(message)s\"",
                    "datefmt": "%Y-%m-%d %H:%M:%SZ",
                }
            error_log_formatter = {
                    "format": """%(levelname)s -->
                                Date/time:      %(asctime)s
                                Process(PID):   %(processName)s (%(process)d)
                                Module:         %(name)s
                                File:           %(filename)s
                                Function:       %(funcName)s
                                At line:        %(lineno)d
                                Description:   "%(message)s" """,
                    "datefmt": "%Y-%m-%d %H:%M:%SZ",
                }