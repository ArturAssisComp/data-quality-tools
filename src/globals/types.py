from enum import Enum


class SnapshotType(Enum):
    # null value inspector tool
    ROW_NULL_DISTRIBUTION_SNAPSHOT = 'row_null_distribution_snapshot'
    COLUMN_NULL_COUNT_SNAPSHOT = 'column_null_count_snapshot'
    COLUMN_PAIR_NULL_PATTERN_SNAPSHOT = 'column_pair_null_pattern_snapshot'
    # data inconsistency inspector tool
    ROW_INCONSISTENCY_DISTRIBUTION_SNAPSHOT = 'row_inconsistency_distribution_snapshot'

class SnapshotMode(Enum):
    INITIAL = 'initial'
    FREE_MODE = 'free-mode'
    STRICT_MODE = 'strict-mode'
    SUBSET_MODE = 'subset-mode'

def get_snapshot_name(type:SnapshotType):
    return type.value.replace('_', '-')

# Consistency check types
class ReservedRuleName(Enum):
    TYPE = 'type'

class ConsistencyCheckConstants(Enum):
    ssBIGINT_MAX_STR =  '9_223_372_036_854_775_807'
    ssBIGINT_MIN_STR =  '-9_223_372_036_854_775_808'
    ssBIGINT_MAX =  9_223_372_036_854_775_807
    ssBIGINT_MIN =  -9_223_372_036_854_775_808

class ConsistencyCheckSpecialRules(Enum):
    NOT_NULL     = '##NOT-NULL##'
    FALSE        = '##FALSE##'
    TRUE         = "##TRUE##"
    

class ConsistencyCheckType(Enum):
    # python types
    STR     = 'STR'
    STRING  = 'STRING'
    INT     = 'INT'
    INTEGER = 'INTEGER'
    FLOAT   = 'FLOAT'
    BOOL    = 'BOOL'
    BOOLEAN = 'BOOLEAN'
    ISO8601_DATE    = 'ISO8601_DATE'
    CHAR = 'CHAR'
    # sql server (all the sql server types are prefixed with ss --> sql server)
    ## Exact numerics
    ssBIGINT   = 'ssBIGINT'
    ssNUMERIC  = 'ssNUMERIC'
    ssBIT      = 'ssBIT'
    ssINT      = 'ssINT'
    ssSMALLINT = 'ssSMALLINT'
    ssDECIMAL  = 'ssDECIMAL'
    ssSMALLMONEY = 'ssSMALLMONEY'
    ssTINYINT = 'ssTINYINT'
    ssMONEY   = 'ssMONEY'
    ## Approximate numerics
    ssFLOAT = 'ssFLOAT'
    ssREAL  = 'ssREAL'
    ## Date and Time
    ssDATE = 'ssDATE'
    ssDATETIMEOFFSET = 'ssDATETIMEOFFSET'
    ssDATETIME       = 'ssDATETIME'
    ssSMALLDATETIME  = 'ssSMALLDATETIME'
    ssTIME = 'ssTIME'
    ## Character strings
    ssCHAR    = 'ssCHAR' 
    ssVARCHAR = 'ssVARCHAR'
    ssTEXT    = 'ssTEXT'
    ## Binary Strings
    ssBINARY    = 'ssBINARY'
    ssVARBINARY = 'ssVARBINARY'