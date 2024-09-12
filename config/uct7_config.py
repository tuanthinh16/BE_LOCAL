from datetime import datetime
import pytz

def TimeUTC7():
    # Tạo đối tượng timezone cho UTC+7
    utc_plus_7 = pytz.timezone('Asia/Bangkok')
    
    # Lấy thời gian hiện tại ở UTC
    utc_now = datetime.utcnow()
    
    # Chuyển đổi thời gian hiện tại từ UTC sang UTC+7
    utc_now = pytz.utc.localize(utc_now)
    local_time = utc_now.astimezone(utc_plus_7)
    
    return local_time

