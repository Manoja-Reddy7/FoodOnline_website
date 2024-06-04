import time,datetime

def get_order_number(pk):
    current_time  = datetime.datetime.now().strftime("%Y%m%d%H%M%S") #2024051145 +pk
    order_number  = current_time + str(pk)
    return order_number