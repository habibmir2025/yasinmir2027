from flask import Flask, request
import requests
from config import TOKEN, API_URL

app = Flask(__name__)

ADMIN_USER_ID = "your_admin_user_id"  # آی‌دی عددی ادمین برای ارسال سفارش‌ها

def send_message(chat_id, text):
    url = f"{API_URL}{TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=data)

@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return "✅ Bale Bot is running!"

    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            send_message(chat_id, "سلام 👋 به ربات hamidmir2027 خوش اومدی.\n\nلطفاً یکی از گزینه‌ها رو تایپ کن:\n\n1. خرید شارژ\n2. بسته اینترنت\n3. ثبت سفارش\n4. اطلاعیه‌ها\n5. پشتیبانی")
        elif text == "1":
            send_message(chat_id, "💳 خرید شارژ\nلطفاً شماره و مبلغ مورد نظر را ارسال کنید.")
        elif text == "2":
            send_message(chat_id, "🌐 خرید بسته اینترنت\nلطفاً شماره و نوع بسته را ارسال کنید.")
        elif text == "3":
            send_message(chat_id, "📝 ثبت سفارش\nلطفاً نوع سفارش، شماره و توضیحات را بنویسید.")
        elif text == "4":
            send_message(chat_id, "ℹ️ اطلاعیه:\nفعلاً اطلاعیه‌ای ثبت نشده.")
        elif text == "5":
            send_message(chat_id, "☎️ برای پشتیبانی با ما در تماس باشید:\n@your_support_username")
        else:
            # ارسال سفارش به ادمین
            requests.post(f"{API_URL}{TOKEN}/sendMessage", json={
                "chat_id": ADMIN_USER_ID,
                "text": f"📥 سفارش جدید:\n\n{text}\n\nاز طرف کاربر: {chat_id}"
            })
            send_message(chat_id, "✅ سفارش شما ثبت شد. در اسرع وقت بررسی می‌شود.")

    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)