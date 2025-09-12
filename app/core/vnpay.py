# Trong file app/core/vnpay.py
import hashlib
import hmac
from urllib.parse import urlencode
from datetime import datetime
from app.core.config import settings

def hmacsha512(key, data):
    byteKey = key.encode('utf-8')
    byteData = data.encode('utf-8')
    return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()

def build_payment_url(order_id: str, amount: int, order_desc: str, ip_addr: str) -> str:
    """
    Xây dựng URL thanh toán cho VNPay.
    """
    vnp_Version = "2.1.0"
    vnp_Command = "pay"
    vnp_TmnCode = settings.VNPAY_TMN_CODE
    vnp_Amount = amount * 100 # VNPay yêu cầu giá trị nguyên, nhân 100
    vnp_CurrCode = "VND"
    vnp_TxnRef = order_id
    vnp_OrderInfo = order_desc
    vnp_OrderType = "other"
    vnp_Locale = "vn"
    vnp_CreateDate = datetime.now().strftime('%Y%m%d%H%M%S')
    vnp_ReturnUrl = settings.VNPAY_RETURN_URL
    vnp_IpAddr = ip_addr

    # Sắp xếp các tham số theo thứ tự alphabet
    input_data = {
        'vnp_Version': vnp_Version,
        'vnp_Command': vnp_Command,
        'vnp_TmnCode': vnp_TmnCode,
        'vnp_Amount': vnp_Amount,
        'vnp_CurrCode': vnp_CurrCode,
        'vnp_CreateDate': vnp_CreateDate,
        'vnp_IpAddr': vnp_IpAddr,
        'vnp_Locale': vnp_Locale,
        'vnp_OrderInfo': vnp_OrderInfo,
        'vnp_OrderType': vnp_OrderType,
        'vnp_ReturnUrl': vnp_ReturnUrl,
        'vnp_TxnRef': vnp_TxnRef,
    }
    
    # Sắp xếp và tạo chuỗi query
    query_string = urlencode(sorted(input_data.items()))
    
    # Tạo chữ ký an toàn
    secure_hash = hmacsha512(settings.VNPAY_HASH_SECRET, query_string)
    
    # Gắn chữ ký vào cuối và trả về URL đầy đủ
    final_url = f"{settings.VNPAY_URL}?{query_string}&vnp_SecureHash={secure_hash}"
    
    return final_url