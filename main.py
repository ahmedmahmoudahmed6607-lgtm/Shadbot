import asyncio
from telethon import TelegramClient, events
from telethon.tl.custom import Button

api_id = '7093128950'
api_hash = '7093128950'
bot_token = '8749774383:AAHFeeU6jJCdfbDNsY-sZUw-omZ41ksennw'

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)


class State:
    def __init__(self):
        self.state = None
        self.message_link = None
        self.report_type = None
        self.custom_message = None
        self.report_count = None
        self.sleep_interval = None

state = State()

main_menu_buttons = [
    [Button.inline("📢 بلاغ على قناة", b"report_channel")],
    [Button.inline("👤 بلاغ على شخص", b"report_user")],
    [Button.inline("👥 بلاغ على جروب", b"report_group")]
]

report_types_buttons = [
    [Button.inline("📣 إزعاج", b"report_spam")],
    [Button.inline("🔪 عنف", b"report_violence")],
    [Button.inline("🚸 إساءة للأطفال", b"report_child_abuse")],
    [Button.inline("💊 مخدرات", b"report_drugs")],
    [Button.inline("🔒 بيانات شخصية", b"report_personal_data")],
    [Button.inline("🔞 إباحية", b"report_pornography")],
    [Button.inline("📝 أخرى", b"report_other")]
]

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("مرحبًا! اختر نوع البلاغ من القائمة أدناه:", buttons=main_menu_buttons)

@client.on(events.CallbackQuery(data=b"report_channel"))
@client.on(events.CallbackQuery(data=b"report_user"))
@client.on(events.CallbackQuery(data=b"report_group"))
async def process_report_type(event):
    await event.respond("أرسل رابط الرسالة التي تريد الإبلاغ عنها:")
    state.state = "awaiting_message_link"

@client.on(events.NewMessage)
async def handle_message(event):
    if state.state == "awaiting_message_link":
        state.message_link = event.text
        await event.respond("اختر نوع البلاغ:", buttons=report_types_buttons)
        state.state = "awaiting_report_type"
    elif state.state == "awaiting_custom_message":
        state.custom_message = event.text
        await event.respond("اختر عدد البلاغات:")
        state.state = "awaiting_report_count"
    elif state.state == "awaiting_report_count":
        state.report_count = int(event.text)
        await event.respond("اختر الفاصل الزمني بين البلاغات (مثال: 10s، 5m، 1h):")
        state.state = "awaiting_sleep_interval"
    elif state.state == "awaiting_sleep_interval":
        state.sleep_interval = event.text
        await send_reports(event)

@client.on(events.CallbackQuery)
async def process_report_reason(event):
    if state.state == "awaiting_report_type":
        state.report_type = event.data.decode('utf-8')
        if state.report_type == "report_other":
            await event.respond("أدخل الرسالة التي تريد إرسالها في البلاغ:")
            state.state = "awaiting_custom_message"
        else:
            await event.respond("اختر عدد البلاغات:")
            state.state = "awaiting_report_count"

async def send_reports(event):
    for i in range(state.report_count):
        await event.respond(f"تم إرسال البلاغ {i+1} من {state.report_count} ✅")
        await asyncio.sleep(parse_time(state.sleep_interval))
    state.state = None

def parse_time(time_str):
    unit = time_str[-1]
    value = int(time_str[:-1])
    if unit == 's':
        return value
    elif unit == 'm':
        return value * 60
    elif unit == 'h':
        return value * 3600
    elif unit == 'd':
        return value * 86400
    else:
        raise ValueError("Invalid time format")

client.start()
client.run_until_disconnected()
