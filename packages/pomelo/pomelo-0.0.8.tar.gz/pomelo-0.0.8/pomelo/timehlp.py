import datetime
import time


def utc2local(utc_st,fmt = None):
    '''UTC时间转本地时间（+8:00)'''
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    if (type(utc_st) == str):
        local_st = datetime.datetime.strptime(utc_st, '%Y-%m-%dT%H:%M:%S%fZ') + offset
    else:
        local_st = utc_st + offset
    if (fmt != None):
        return local_st.strftime(fmt)
    else:
        return local_st


def local2utc(local_st):
    '''本地时间转UTC时间（-8:00）'''
    time_struct = time.mktime(local_st.timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st    

'''
    end_tm 默认为当前时间
    from_tm 可以时间戳1541038591 或者 '2018-11-01 10:26:30'，'2018-11-01T00:09:36Z'
    from_fmt 只有当from_tm为字符时候才生效，默认是'%Y-%m-%dT%H:%M:%S%fZ'，例如：'%Y-%m-%d %H:%M:%S'
    end_fmt 同上
'''
def diff(from_tm,end_tm = None,from_fmt = None,end_fmt = None):
    from_dt = None
    if type(from_tm) == float or type(from_tm) == int:
        from_dt = datetime.datetime.fromtimestamp(from_tm)
    elif type(from_tm) == str:
        if (from_fmt != None):
            from_dt = datetime.datetime.strptime(from_tm,from_fmt)
        else:
            from_dt = datetime.datetime.strptime(from_tm,'%Y-%m-%dT%H:%M:%S%fZ')
    end_dt = None
    if (end_tm != None):
        if type(end_tm) == float or type(end_tm) == int:
            end_dt = datetime.datetime.fromtimestamp(end_tm)
        elif type(end_tm) == str:
            if (end_fmt != None):
                end_dt = datetime.datetime.strptime(end_tm,end_fmt)
            else:
                end_dt = datetime.datetime.strptime(end_tm,'%Y-%m-%dT%H:%M:%S%fZ')
    else:
        end_dt = datetime.datetime.fromtimestamp(time.time())
    return (end_dt - from_dt).seconds



if __name__ == '__main__':
    l_stp = time.time()
    l_tm = datetime.datetime.fromtimestamp(l_stp)
    print(local2utc(l_tm))
    utc_dt = datetime.datetime.strptime('2018-11-01T00:09:36Z', '%Y-%m-%dT%H:%M:%S%fZ')
    print(utc2local(utc_dt))
    print(utc2local('2018-11-01T00:09:36Z'))
    print(utc2local(utc_dt,'%Y-%m-%d %H:%M:%S'))
    print(diff('2018-11-01T00:09:36Z'))
    print(diff('2018-11-01 10:26:30',None,'%Y-%m-%d %H:%M:%S'))



