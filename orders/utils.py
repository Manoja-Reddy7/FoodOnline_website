import time,datetime
import simplejson as json

def get_order_number(pk):
    current_time  = datetime.datetime.now().strftime("%Y%m%d%H%M%S") #2024051145 +pk
    order_number  = current_time + str(pk)
    return order_number

def order_total_by_vendor(order,vendor_id):
     total_data   = json.loads(order.total_data)
     data         = total_data.get(str(vendor_id))
     subtotal  = 0
     tax  = 0
     tax_dict  = {}
     
     for key,val in data.items():
                subtotal += float(key)
                val = val.replace("'",'"')
                val = json.loads(val)
                tax_dict.update(val)
           
                # Caluculate tax
                for i in val:
                    for j in val[i]:
                        tax += float(val[i][j])
                        
     grand_total     = float(subtotal) + float(tax)
        
      
     context  = {
            'grand_total' : grand_total,
            'tax_dict'   : tax_dict,
            'subtotal'   : subtotal,
        }
     
     return context