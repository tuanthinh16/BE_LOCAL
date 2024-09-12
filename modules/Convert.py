import datetime

def SystemTimeToTimeNumber(time: datetime.datetime) -> int:
    """
    Convert a datetime object to a 14-digit integer in the format yyyymmddhhmmss.
    
    :param time: datetime object to be converted
    :return: 14-digit integer representing the time
    """
    return int(time.strftime('%Y%m%d%H%M%S'))

def TimeNumberToTimeString(time: int) -> datetime.datetime:
    """
    Convert a 14-digit integer in the format yyyymmddhhmmss to a datetime object.
    
    :param time: 14-digit integer representing the time
    :return: datetime object
    """
    time_str = str(time)
    return datetime.datetime.strptime(time_str, '%Y%m%d%H%M%S')

def TimeNumberToDateString(time: int) -> str:
    """
    Convert a 14-digit integer in the format yyyymmddhhmmss to a formatted date string.
    
    :param time: 14-digit integer representing the time
    :return: formatted date string in the format yyyy/mm/dd - hh:mm:ss
    """
    time_str = str(time)
    dt = datetime.datetime.strptime(time_str, '%Y%m%d%H%M%S')
    return dt.strftime('%Y/%m/%d - %H:%M:%S')