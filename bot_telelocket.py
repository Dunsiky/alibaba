from telegram.ext import Updater, CommandHandler
import random
from zLocket_Tool import zLocket, format_proxy

TOKEN = "7875782404:AAGwsnvDsCZtHCkrqBrkxviBJ1nXpA0AAak"  # Điền token Bot Telegram của bạn

def load_proxies():
    with open('proxy.txt', 'r') as f:
        return [line.strip() for line in f if ':' in line]

def random_icons(n=3):
    ICON_LIST = [
        '😀','🤣','😂','😄','😃','😋','😅','😗','☺️','😊','😑','😐','😙','😍','😣','😜','😛','😥','😕','😝','😴',
        '🤑','😌','🤯','🙁','😩','😤','😟','😓','😦','😳','🥶','🤒','🤕','😱','🤪','🤫','🤓','💀','☠️','🤭','😽','😾',
        '🤖','👦','👧','🧑','🧒','👶','👩‍⚕️','👩‍🏫','🧓','👨‍⚖️','👨‍🏭','👨‍🏫','👩‍🔧','👩‍🏭','👨‍💻','👨‍🍳','👩‍🔧','👩‍💻'
    ]
    return ''.join(random.choices(ICON_LIST, k=n))

def start(update, context):
    update.message.reply_text(
        "HDSD:\n"
        "/spam <username> <số_lần> <nội_dung_text>\n"
        "VD: /spam abcxyz 20 iu dương\n"
        "Mỗi lần spam sẽ gửi text + 3 icon random, 10 lần đổi proxy một lần.\n"
        "/proxylist: xem danh sách proxy đang có."
    )

def spam(update, context):
    args = context.args
    if len(args) < 3:
        update.message.reply_text("Dùng đúng: /spam <username> <số_lần> <nội_dung_text>\nVD: /spam duyboy 20 iu dương")
        return
    username = args[0]
    try:
        nspam = int(args[1])
        if nspam <= 0 or nspam > 100:
            update.message.reply_text("Số lần spam hợp lệ: 1-100.")
            return
    except:
        update.message.reply_text("Số lần spam phải là số!")
        return

    text_message = ' '.join(args[2:])
    proxies = load_proxies()
    if not proxies:
        update.message.reply_text("proxy.txt không có proxy nào!")
        return

    zl = zLocket(target_friend_uid=username)
    ok = 0
    for i in range(nspam):
        if i % 10 == 0:
            proxy_str = random.choice(proxies)
            proxy_dict = format_proxy(proxy_str)
        content = f"{text_message} {random_icons(3)}"
        res = zl.excute(
            zl.API_LOCKET_URL + "/sendFriendRequest",
            headers=zl.headers_locket(),
            payload={
                "data": {
                    "user_uid": username,
                    "source": "signUp",
                    "platform": "iOS",
                    "message": content   # Nếu API không hỗ trợ trường message thì comment hoặc sửa lại trường cho đúng API thực tế
                }
            },
            proxies_dict=proxy_dict
        )
        if isinstance(res, dict):
            ok += 1
    update.message.reply_text(
        f"Đã gửi {ok}/{nspam} request tới {username} (nội dung: {text_message} + 3 icon random, mỗi 10 lần đổi proxy)."
    )

def proxylist(update, context):
    try:
        proxies = load_proxies()
    except:
        proxies = []
    if not proxies:
        update.message.reply_text("proxy.txt rỗng hoặc lỗi!")
    else:
        update.message.reply_text(f"Đã nạp {len(proxies)} proxy, không hiển thị chi tiết!")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("spam", spam))
    dp.add_handler(CommandHandler("proxylist", proxylist))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
