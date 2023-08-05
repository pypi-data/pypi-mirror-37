""" tittles.tittles 180809_1100
        171215_1700
"""

import logging
import sys, re


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s: %(module)s:%(lineno)d(%(funcName)s) %(message)s", level=logging.DEBUG)
_log = logging.getLogger(__name__)


class ConfigError(Exception): pass


class OperationError(Exception): pass


class LogError(Exception): pass


class ModuleRefreshError(Exception): pass


class DbError(Exception): pass


class DbConnectError(DbError): pass


class DbExecuteError(DbError): pass


class DbIntgrError(DbError): pass


def msg_exc(msg, myexc_class=None):
    """My exception with traceback"""
    # Retrieve exception info
    exc_info_ = sys.exc_info()
    # Set exception class
    cls_ = Exception.__class__
    if myexc_class:
        cls_ = myexc_class
    elif exc_info_ and exc_info_[0]:
        cls_ = exc_info_[0]
    # Set exception message
    msg_ = msg or ""
    if exc_info_ and exc_info_[1]:
        msg_ += (": %s" % (exc_info_[1], ))
    exc_ = cls_(msg_)
    if exc_info_ and exc_info_[2]:
        exc_.__traceback__ = exc_info_[2]
    return exc_


def ifnull(var, default):
    """Return variable value or default"""
    return var if var else default


def nvl(var, default):
    """Synonym for 'ifnull' function"""
    return ifnull(var, default)


def list_or_value_to_string(var, sep=" "):
    """Convert list or tuple or value to string"""
    if isinstance(var, (list, tuple)):
        return sep.join(str(v) for v in var)
    return str(var)


def lovts(var, sep=" "):
    """Short name for 'list_or_value_to_string(var, sep=" ")'"""
    return list_or_value_to_string(var, sep)


def dicarray_list_prefixed_values(dica, prefix, key):
    """Compose list of prefixed dica values for the given key"""
    values_ = []
    for d_ in dica:
        values_.append(prefix + d_.get(key, ""))
    return values_


def dalpv(dicarray, prefix, key):
    """Short name for 'dicarray_list_prefixed_values(dica, prefix, key)'"""
    return dicarray_list_prefixed_values(dicarray, prefix, key)


def dicarray_list_values(dica, key):
    """Compose list of dica values for the key given"""
    return dicarray_list_prefixed_values(dica, "", key)


def dalv(dica, key):
    """Short name for 'dicarray_list_values(dica, key)'"""
    return dicarray_list_values(dica, key)


def dicarray_dic_index_by_value(dica, key, value):
    """Retrieve dic index in dicarray with key-value pair"""
    i_ = 0
    for d_ in dica:
        if d_.get(key) == value: return i_
        i_ += 1
    return -1


def dadibv(dica, key, value):
    """Short name for 'dicarray_dic_index_by_value(dica, key, value)'"""
    return dicarray_dic_index_by_value(dica, key, value)


def tuparray_value_by_index(tupa, i):
    """Compose list of indexed values from tupa"""
    v_ = []
    for t_ in tupa:
        v_.append(t_[i])
    return v_


def tavbi(tuparray, i):
    """Short name for 'tuparray_value_by_index(tupa, i)'"""
    return tuparray_value_by_index(tuparray, i)


def dicarray_find_key_value(dica, key, value):
    """Find dics in dicarray with [key: value] pair."""
    dics_ = []
    for d_ in dica:
        if isinstance(d_, dict) and d_.get(key) == value:
            dics_.append(d_)
    return dics_


def dafkv(dica, dic_key, dic_value):
    """Short name for 'dicarray_find_key_value(dica, key, value)'"""
    return dicarray_find_key_value(dica, dic_key, dic_value)


def dicarray_find_first_key_value(dica, key, value):
    """Find first dic entry in dicarray with [key: value] pair."""
    for d_ in dica:
        if isinstance(d_, dict) and d_.get(key) == value:
            return d_


def daffkv(dica, key, value):
    """Short name for 'dicarray_find_first_key_value(dica, key, value)'"""
    return dicarray_find_first_key_value(dica, key, value)


def dicarray_dup_key(dica, orig_key, dest_key):
    """Duplicate dicarray values from orig_key to dest_key"""
    for d_ in dica:
        if isinstance(d_, dict):
            v_ = d_.get(orig_key)
            if v_: d_[dest_key] = v_
    return dica


def dic_cmp(dic1, dic2):
    """Compare dictionaries"""
    d1_keys_ = set(dic1.keys())
    d2_keys_ = set(dic2.keys())
    intersect_keys_ = d1_keys_.intersection(d2_keys_)
    added_ = d1_keys_ - d2_keys_
    removed_ = d2_keys_ - d1_keys_
    modified_ = []
    same_ = []
    for k_ in intersect_keys_:
        if dic1[k_] == dic2[k_]:
            same_.append(k_)
        else:
            modified_.append({k_: (dic1[k_], dic2[k_])})
    return added_, removed_, modified_, same_


def dic_eq(dic1, dic2):
    """Verify dictionaries are equal"""
    added_, removed_, modified_, dummy = dic_cmp(dic1, dic2)
    if not (added_ or removed_ or modified_):
        return True
    return False


def dict_is_equal(dic1, dic2):
    """Verify dictionaries are equal. Synonym to dic_eq(dic1, dic2)"""
    return dic_eq(dic1, dic2)


def list_filter_regex(list, regex):
    rec_ = re.compile(regex)
    return [i_ for i_ in list if not rec_.search(i_)]


if __name__ == "__main__":

    # def test_dic_cmp():
    #     """Test dic_cmp"""
    #     dic1_ = dict(a=1, b=2, c=3, d=4)
    #     dic2_ = dict(a=1, b=2, c=3, d=5)
    #     add_, rem_, mod_, eq_ = dic_cmp(dic1_, dic2_)
    #     _log.debug("added=%s, removed=%s, modified=%s, same=%s.", add_, rem_, mod_, eq_)
    #     _log.debug("is_equal=%s", dic_eq(dic1_, dic2_))

    # def test_lovts():
    #     # import inspect
    #     """Test 'lovts'"""
    #     a_ = "one-two-three"
    #     # _log.debug("C: %s", inspect.getmro(a_))
    #     _log.debug("lovts_1: %s", lovts(a_))

    # test_lovts()

    li_ = ["r$_create_dt", "one", "two", "three", "four", "five", "r$_op", "more than five", "much larger value", "r$_id"]

    _log.debug("all=%s; filtered=%s;", li_, list_filter_regex(li_, "^" + re.escape("r$_")))
