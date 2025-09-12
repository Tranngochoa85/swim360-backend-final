import stripe
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.core.config import settings
from app.api.v1.dependencies import get_current_user
from supabase import Client
from app.core.supabase_client import supabase
from pydantic import BaseModel
from uuid import UUID
from app.core.vnpay import build_payment_url # Import hàm mới của chúng ta

router = APIRouter()
stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentIntentCreate(BaseModel):
    offer_id: UUID

# Endpoint cho Stripe (giữ nguyên)
@router.post("/create-stripe-intent")
def create_stripe_payment_intent(
    # ... code cũ của Stripe ...
):
    pass # Giữ lại để tham khảo, hoặc xóa đi nếu không dùng

# --- ENDPOINT MỚI CHO VNPAY ---
@router.post("/create-vnpay-url")
def create_vnpay_payment_url(
    intent_data: PaymentIntentCreate,
    request: Request, # FastAPI sẽ tự động cung cấp đối tượng request
    db: Client = Depends(lambda: supabase),
    current_user = Depends(get_current_user)
):
    """
    Tạo một đường dẫn thanh toán VNPay.
    """
    try:
        # 1. Lấy thông tin giá tiền từ offer trong DB
        offer_res = db.table("course_offers").select("price").eq("id", str(intent_data.offer_id)).single().execute()
        if not offer_res.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy ưu đãi hợp lệ.")
        
        amount_in_vnd = int(offer_res.data['price'])

        # 2. Tạo một giao dịch 'pending' trong "sổ kế toán"
        transaction_res = db.table("transactions").insert({
            "user_id": str(current_user.id),
            "course_offer_id": str(intent_data.offer_id),
            "amount": amount_in_vnd,
            "currency": "vnd",
            "status": "pending",
            "gateway": "vnpay" # Ghi rõ cổng là vnpay
        }).execute()

        if not transaction_res.data:
            raise HTTPException(status_code=500, detail="Không thể tạo giao dịch trong hệ thống.")
        
        transaction_id = transaction_res.data[0]['id']
        
        # 3. Lấy IP của người dùng từ request
        client_ip = request.client.host
        
        # 4. Gọi hàm helper để xây dựng URL
        payment_url = build_payment_url(
            order_id=str(transaction_id),
            amount=amount_in_vnd,
            order_desc=f"Thanh toan khoa hoc Swim360 - Ma GD: {transaction_id}",
            ip_addr=client_ip
        )
        
        # 5. Trả về URL cho Frontend
        return {"paymentUrl": payment_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))