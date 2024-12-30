import asyncio
from telethon.errors import FloodWaitError, SessionPasswordNeededError
from telethon import TelegramClient, events, Button, utils
from telethon.sessions import StringSession
import json
import os
import re
import time

api_id = 21641452
api_hash = '0926f487616f4545937c65b5e8ea544c'
bot_token = '7363238502:AAFO8WC1ulCN7w2AIN0txDymUOufHmH0t6g'
session = "1BJWap1wBu5hWRnNWCupBSg2JGixXThlKKQaQfOc6RssMCnyo61FZMLKsNA8OJkgqxLIUK7TufOfCVj6xoqTrKIKs7p-wUbmvXTmitIIbjVJrHlEdIGXqK-RndFi6jvU7qOT15pajkMstnEKQGs4o8ISo9xB-tgrTjRCu3g3w4HyDIIne8EBBjdnw5RZ4LEAJJVMdnz42SGuMxSkQ6HOrQAU1vDkeen1O9LBN_bjczA3XZWY0Rv2pOYY0oJE1b1IJGtfSVsVuP5esB3w-TwTmWju2BKMdluuFv30YIEYOTlcwLWWMrLYWmU9ipa6W-I8S1cSZVbAODUF-ukueI57AbotAmMDyXY8="
client = TelegramClient('WaD', api_id, api_hash)
the_owner = 6590885543
free_mod = True
blocked_users = []
BLOCKED_USERES_FILE = 'data/blocked_users.json'

if os.path.exists(BLOCKED_USERES_FILE):
    try:
        with open(BLOCKED_USERES_FILE, "r") as f:
            blocked_users = json.load(f)
    except:
        print(f"Error loading blocked users")
else:
    try:
        with open(BLOCKED_USERES_FILE, "w") as f:
            user_data = [1, 2]
            json.dump(user_data, f)
    except:
        print(f"Error Upload blocked users file")

@client.on(events.NewMessage(pattern='/owner_pannel'))
async def owner_pannel(event):
    is_blocked = await check_block(event)
    if is_blocked:
        return
    await event.respond('- اهلا بك في لوحة التحكم .', buttons=[
        [Button.inline('‹ تفعيل الوضع المجاني ›', data='enable_free'),
         Button.inline('‹ تعطيل الوضع المجاني ›', data='disable_free')],
        [Button.inline('‹ راديو للمستخدمين ›', data='radio_users')],
        [Button.inline('‹ حظر المستخدم ›', data='block_user'),
         Button.inline('‹ رفع الحظر عن المستخدم ›', data='unblock_user')],
        [Button.inline('‹ الحصول على قاعدة بيانات المستخدمين ›', data='get_database')],
        [Button.inline('‹ اضافة VIP لمستخدم ›', data='vip_user'),
         Button.inline('‹ إلغاء VIP لمستخدم ›', data='unvip_user')],
        [Button.url('‹ Developer ›', 't.me/MM_GM')],
    ])


@client.on(events.CallbackQuery(pattern='pannel'))
async def owner_pannel_ed(event):
    is_blocked = await check_block(event)
    if is_blocked:
        return
    await event.edit('- اهلا بك في لوحة التحكم .', buttons=[
        [Button.inline('‹ تفعيل الوضع المجاني ›', data='enable_free'),
         Button.inline('‹ تعطيل الوضع المجاني ›', data='disable_free')],
        [Button.inline('‹ راديو للمستخدمين ›', data='radio_users')],
        [Button.inline('‹ حظر المستخدم ›', data='block_user'),
         Button.inline('‹ رفع الحظر عن المستخدم ›', data='unblock_user')],
        [Button.inline('‹ الحصول على قاعدة بيانات المستخدمين ›', data='get_database')],
        [Button.inline('‹ اضافة VIP لمستخدم ›', data='vip_user'),
         Button.inline('‹ إلغاء VIP لمستخدم ›', data='unvip_user')],
        [Button.url('‹ Developer ›', 't.me/MM_GM')],
    ])




async def enable_free_mod(event):
    global free_mod
    free_mod = True
    await event.edit("- تم تفعيل الوضع المجاني .", buttons=[Button.inline("‹ رجوع ›", data='pannel')])

async def disable_free_mod(event):
    global free_mod
    free_mod = False
    await event.edit("تم تعطيل الوضع المجاني.", buttons=[Button.inline("‹ رجوع ›", data='pannel')])

async def radio_for_users(event):
    async with client.conversation(event.chat_id) as conv:
        cancel_button = Button.inline("رجوع", b'cancel')
        await conv.send_message('ارسل الرسالة التي تود ارسالها لجميع المستخدمين\nللالغاء ارسل /cancel', buttons=cancel_button)
        response = await conv.wait_event(events.NewMessage(from_users=event.sender_id))
        if response.raw_text == '/cancel':
            await event.respond('تم الغاء العملية')
            return
        message_to_send = (await conv.get_response()).text
        for filename in os.listdir('users'):
            if filename.endswith('.json'):
                user_id = os.path.splitext(filename)[0]
                user_id = int(user_id)
                await send_message(message_to_send, user_id)

        await conv.send_message('جاري ارسال الرسالة لجميع المستخدمين', buttons=[Button.inline("‹ رجوع ›", data='pannel')])

async def send_message(message_to_send, user_id):
    await client.send_message(user_id, message_to_send)

async def block_user(event):
    async with client.conversation(event.chat_id) as conv:
        await event.delete()
        await conv.send_message('- ارسل ايدي الشخص الذي تود حظره .')
        response = await conv.get_response()
        id_to = response.text
        try:
            id_to_block = int(id_to)
            try:
                if id_to_block == the_owner:
                    await event.respond("- لا يمكنك حظر مالك البوت. -", buttons=[Button.inline("‹ رجوع ›", data='pannel')])
                    return

                blocked_users.append(id_to_block)
                with open(BLOCKED_USERES_FILE, "w") as f:
                    json.dump(blocked_users, f)

                await event.respond(f"- تم حظر المستخدم {id_to_block} .", buttons=[Button.inline("‹ رجوع ›", data='pannel')])
                await client.send_message(id_to_block, '- تم حظرك من قبل المطور .', buttons=[Button.url('‹ Developer ›', 't.me/MM_GM')])
            except ValueError:
                await event.respond("هذا ليس معرف مستخدم صحيح.", buttons=[Button.inline("‹ رجوع ›", data='pannel')])
            except Exception as e:
                await event.respond(f"حدث خطأ أثناء حظر المستخدم : {e}", buttons=[Button.inline("‹ رجوع ›", data='pannel')])

        except ValueError:
            await event.respond("الرجاء إدخال معرف مستخدم صحيح (رقم).", buttons=[Button.inline("‹ رجوع ›", data='pannel')])
        except Exception as e:
            await event.respond(f"حدث خطأ غير متوقع: {e}", buttons=[Button.inline("‹ رجوع ›", data='pannel')])

async def unblock_user(event):
    async with client.conversation(event.chat_id) as conv:
        await event.delete()
        await conv.send_message('ارسل ايدي الشخص الذي تود الغاء حظره')
        response = await conv.get_response()
        id_to = response.text
        try:
            id_to_unblock = int(id_to)
            if id_to_unblock in blocked_users:
                blocked_users.remove(id_to_unblock)
                with open(BLOCKED_USERES_FILE, "w") as f:
                    json.dump(blocked_users, f)
                await event.respond(f"تم إلغاء حظر المستخدم {id_to_unblock}", buttons=[Button.inline("‹ رجوع ›", data='pannel')])
                await client.send_message(id_to_unblock, '- تم رفع الحظر عن حسابك .', buttons=[Button.url('‹ Developer ›', 't.me/MM_GM')])
            else:
                await event.respond(f"المستخدم {id_to_unblock} ليس محظورا.", buttons=[Button.inline("‹ رجوع ›", data='pannel')])
        except ValueError:
            await event.respond("الرجاء إدخال معرف مستخدم صحيح (رقم).", buttons=[Button.inline("‹ رجوع ›", data='pannel')])
        except Exception as e:
            await event.respond(f"حدث خطأ غير متوقع: {e}", buttons=[Button.inline("‹ رجوع ›", data='pannel')])

async def get_user_database(event):
    async with client.conversation(event.chat_id) as conv:
        await event.delete()
        await conv.send_message('ارسل معرف الشخص الذي تود جلب بياناته')
        user_id = (await conv.get_response()).text
        try:
            user_id = int(user_id)
        except ValueError:
            await event.respond('ارسل معرف صالح', buttons=[Button.inline("‹ رجوع ›", data='pannel')])
        file_path = f"users/{user_id}.json"
        try:
            with open(f'{file_path}', "rb") as f:
                await conv.send_file(f, caption="هذه هي قاعدة البيانات", buttons=[Button.inline("‹ رجوع ›", data='pannel')])
        except:
            await event.respond(f'المستخدم {user_id} غير موجود بالبوت', buttons=[Button.inline("‹ رجوع ›", data='pannel')])

async def vip_for_user(event):
    async with client.conversation(event.chat_id) as conv:
        await conv.send_message('- ارسل ايدي الشخص الذي تود منحه VIP .')
        vip_user = (await conv.get_response()).text
        try:
            vip_user = int(vip_user)
        except ValueError:
            await event.respond('- الايدي غير صحيح .', buttons=[Button.inline("‹ رجوع ›", data='pannel')])
            return
        
        file_path = f"users/{vip_user}.json"
        try:
            with open(file_path, "r+") as f:
                user_data = json.load(f)
                user_data["vip"] = True
                f.seek(0) 
                json.dump(user_data, f, indent=4)
                f.truncate()
            await event.respond(f'تم منح VIP للمستخدم {vip_user}.')
        except FileNotFoundError:
            await event.respond('- لم يتم العثور على بيانات المستخدم.', buttons=[Button.inline("‹ رجوع ›", data='pannel')])
        except Exception as e:
            await event.respond(f'- حدث خطأ: {str(e)}', buttons=[Button.inline("‹ رجوع ›", data='pannel')])

async def unvip_for_user(event):
    async with client.conversation(event.chat_id) as conv:
        await conv.send_message('- ارسل ايدي الشخص الذي تود ازالة منه VIP .')
        unvip_user = (await conv.get_response()).text
        try:
            unvip_user = int(unvip_user)
        except ValueError:
            await event.respond('- الايدي غير صحيح .', buttons=[Button.inline("‹ رجوع ›", data='pannel')])
            return
        
        file_path = f"users/{unvip_user}.json"
        try:
            with open(file_path, "r+") as f:
                user_data = json.load(f)
                user_data["vip"] = False
                f.seek(0)
                json.dump(user_data, f, indent=4)
                f.truncate() 
            await event.respond(f'تم إلغاء VIP عن المستخدم {unvip_user}.')
        except FileNotFoundError:
            await event.respond('- لم يتم العثور على بيانات المستخدم.', buttons=[Button.inline("‹ رجوع ›", data='pannel')])
        except Exception as e:
            await event.respond(f'- حدث خطأ: {str(e)}', buttons=[Button.inline("‹ رجوع ›", data='pannel')])

async def vip_prices(event):
    await event.edit("""
    ✿ أسعار الأشتراك VIP :
 
- اسبوع ~> 3$ ( Asiacell / USD ) .
- اسبوعين ~> 5$ ( Asiacell / USD ) .
- شهر ~> 6$ ( Asiacell / USD ) .
    """, buttons=[Button.url('‹ المطور ›', 't.me/MM_GM')],)
    return

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
        
    user_id = event.sender_id
    user_data_file = 'users/' + str(user_id) + ".json"

    if os.path.exists(user_data_file):
        with open(user_data_file, 'r') as f:
            user_data = json.load(f)
    else:
        user_data = {
    "vip": False,
    "session": "",
    "added_group": "",
    "collect_status": False,
    "tip": {
        "status": False
      },
      "salary": {
        "status": False
      },
      "invest": {
        "value": 0,
        "status": False
      }
    }
    with open(user_data_file, 'w') as f:
        json.dump(user_data, f, indent=4)

    if free_mod:
        await handle_start(event)
        return

    elif user_data["vip"]:
        await handle_start(event)
        return

    elif not free_mod:
        if not user_data["vip"]:
            await event.respond('‹ الوضع المجاني مغلق ›\n‹ تستطيع الاشتراك عن طريق مراسلة المطور ›', buttons=[
                [Button.inline('‹ اسعار الاشتراك ›', 'vip_prices')],
                [Button.url('‹ المطور ›', 't.me/MM_GM')],
            ])




@client.on(events.CallbackQuery())
async def callback_handler(event):
    user_id = event.sender_id
    user_data_file = f"users/{user_id}.json"
    data = event.data.decode()
    is_blocked = await check_block(event)
    if is_blocked:
        return
    
    if data == 'enable_free':
        await enable_free_mod(event)
        return
    elif data == 'disable_free':
        await disable_free_mod(event)
        return
    elif data == 'radio_users':
        await radio_for_users(event)
        return
    elif data == 'block_user':
        await block_user(event)
        return
    elif data == 'unblock_user':
        await unblock_user(event)
        return
    elif data == 'get_database':
        await get_user_database(event)
        return
    elif data == 'vip_user':
        await vip_for_user(event)
        return
    elif data == 'unvip_user':
        await unvip_for_user(event)
        return
    elif data == 'vip_prices':
        await vip_prices(event)
        return
    elif data == 'pannel':
        await owner_pannel_ed(event)
        return
    
    with open(user_data_file, 'r') as f:
        user_data = json.load(f)
    if user_data["vip"] == False:
        if not free_mod:
            await event.edit('‹ الوضع المجاني مغلق ›\n‹ تستطيع الاشتراك عن طريق مراسلة المطور ›', buttons=[
                    [Button.inline('‹ اسعار الاشتراك ›', 'vip_prices')],
                    [Button.url('‹ المطور ›', 't.me/MM_GM')],  
            ])
            return

    if data == 'add':
        await handle_add(event)
    elif data == 'add_group':
        await handle_add_group(event)
    elif data == 'add_account':
        await handle_add_account(event)
    elif data == 'add_account_session':
        await handle_add_account_session(event)
    elif data == 'add_account_phone':
        await handle_add_account_phone(event)
    elif data == 'tip':
        if user_data["session"] == "":
            await event.answer('- لم تقم بتسجيل الدخول .', alert=True)
            return
        await handle_tip(event)
    elif data == 'tip_off':
        if user_data["session"] == "":
            await event.answer('- لم تقم بتسجيل الدخول .', alert=True)
            return
        await handle_tip_off(event)
    elif data == 'salary':
        if user_data["session"] == "":
            await event.answer('- لم تقم بتسجيل الدخول .', alert=True)
            return
        await handle_salary(event)
    elif data == 'salary_off':
        if user_data["session"] == "":
            await event.answer('- لم تقم بتسجيل الدخول .', alert=True)
            return
        await handle_salary_off(event)
    elif data == 'invest':
        await handle_invest(event)
    elif data == 'set_invest':
        if user_data["session"] == "":
            await event.answer('- لم تقم بتسجيل الدخول .', alert=True)
            return        
        await handle_set_invest(event)
    elif data == 'auto_invest_on':
        if user_data["session"] == "":
            await event.answer('- لم تقم بتسجيل الدخول .', alert=True)
            return
        await handle_auto_invest_on(event)    
    elif data == 'auto_invest_off':
        if user_data["session"] == "":
            await event.answer('- لم تقم بتسجيل الدخول .', alert=True)
            return
        await handle_auto_invest_off(event)
    elif data == 'delete_invest':
        if user_data["session"] == "":
            await event.answer('- لم تقم بتسجيل الدخول .', alert=True)
            return
        await handle_delete_invest(event)
    elif data == 'on_collect':
        await collect_handler.handle_on_collect(event)
    elif data == 'off_collect':
        await collect_handler.handle_off_collect(event)
    elif data == 'back':
        await update_buttons(event)
    elif data == 'bank_information':
        await bank_information(event)
    elif data == 'delete_account':
        await delete_account(event)     
    elif data == 'change_Account':
        await change_Account(event)
    elif data == 'money_top':
        await money_top(event)
    elif data == 'transfer_amounts':
        await transfer_amounts(event)
    elif data == 'convert_Session':
        await handle_convert_session(event)
    elif data == 'convert_phone':
        await handle_convert_phone(event)

async def handle_add(event):
    await event.edit('- تستطيع اضافة ماتريد من الاسفل .\n``` تستطيع اضافة حساب الى البوت```\n```تستطيع ايضا اضافة المجموعة التي تود التجميع بها```', buttons=[
        [Button.inline('‹ إضافة مجموعة ›', data=b'add_group'), Button.inline('‹ إضافة حساب ›', data=b'add_account')],
        [Button.inline('‹ رجوع ›', 'back')]
    ])
async def handle_add_group(event):
    async with client.conversation(event.chat_id) as conv:
        user_id = event.sender_id
        user_data_file = f"users/{user_id}.json"

        if not os.path.exists(user_data_file):
            user_data = {"added_group": None}
        else:
            with open(user_data_file, 'r') as f:
                user_data = json.load(f)

        await event.edit('- ارسل معرف المجموعة مبدوء بـ (-) :\n```مثال : 1234567890123-```\nللالغاء ارسل - ( /cancel ) .')
        group_input = await conv.wait_event(events.NewMessage(from_users=event.sender_id))
        group_input = group_input.text
        if group_input.lower() == "/cancel":
            await event.respond('- تم الغاء العملية .', buttons=[[Button.inline("‹ رجوع ›", data='add')]])
            return
        elif not re.fullmatch(r"-\d+", group_input):
            await event.respond('يجب ان يبدأ معرف المجموعة بـ ( - ) خطأ :', buttons=[[Button.inline("‹ رجوع ›", data='add')]])
            return
        
        user_data["added_group"] = group_input 
        with open(user_data_file, 'w') as f:
            json.dump(user_data, f, indent=4)
        await event.respond(f'- تمت إضافة المجموعة بنجاح : ```( {group_input} )```', buttons=[[Button.inline("‹ رجوع ›", data='back')]])

async def handle_add_account(event):
    user_id = event.sender_id
    user_data_file = 'users/' + str(user_id) + ".json"
    with open(user_data_file, 'r') as f:
        user_data = json.load(f)
    if user_data["session"] != "":
        await event.edit('```- لقد قمت باضافة حساب مسبقا .```',buttons=[[Button.inline('‹ حذف الحساب ›', 'delete_account'), Button.inline('‹ تغيير الحساب ›', 'change_Account')],[Button.inline('‹ رجوع ›', 'add')],])
        return
    try:
        with open(user_data_file, 'r') as f:
            user_data = json.load(f)

        await event.edit("""
        - لديك طريقتين لأضافة حساب تيليجرام الى البوت !
        ```االطريقة الاولى : عن طريق رقم الهاتف سيتم طلب كود التسجيل الى حسابك \n سيتم طلب رمز التحقق بخطوتين ان وجد```
 
        ``` الطريقة الثانية : عن طريق كود جلسة التليثون ( السيشن ) ```
 
        **ملاحظة هامة لاعزائي المستخدمين **:
        نود أن نؤكد لك أن بيانات حسابك الشخصية محمية تمامًا ولن يتم فتحها أو مشاركتها مع أي جهة خارجية دون إذنك.
        نحن نلتزم بأعلى معايير الأمان والخصوصية لحماية معلوماتك
        شكرًا لثقتك بنا .
        """, buttons=[
            [Button.inline('‹ استخدام سيشن جلسة ›', data=b'add_account_session'), Button.inline('‹ استخدام رقم الهاتف ›', data=b'add_account_phone')],
            [Button.inline('‹ رجوع ›', 'back')]
        ])

    except (FileNotFoundError, json.JSONDecodeError) as e:
        await event.respond(f"حدث خطأ: {e}")

async def handle_add_account_session(event):
    async with client.conversation(event.chat_id) as conv:
        user_id = event.sender_id
        user_data_file = 'users/' + str(user_id) + ".json"
        with open(user_data_file, 'r') as f:
            user_data = json.load(f)
        if user_data["session"] != "":
            await event.edit('```- لقد قمت باضافة حساب مسبقا .```', buttons=[[Button.inline('‹ حذف الحساب ›', 'delete_account'), Button.inline('‹ تغيير الحساب ›', 'change_Account')],[Button.inline('‹ رجوع ›', 'add')],])
            return
        try:
            await event.edit("""
            ```- أرسل كود الجلسة ( السيشن ) الخاص بحساب التليكرام ! ```
            - للألغاء ارسل ( /cancel ) .""")

            message = await conv.wait_event(events.NewMessage(
                from_users=event.sender_id, chats=event.chat_id
            ), timeout=30)

            session_code = message.text.strip()
            if session_code.lower() == "/cancel":
                await event.respond('- تم الغاء العملية .', buttons=[[Button.inline("‹ رجوع ›", data='add_account')]])
                return
            try:
                await CheckClient(session_code, event)
                if CheckClient:
                    try:
                        with open(user_data_file, 'r') as f:
                            user_data = json.load(f)
                        user_data["session"] = session_code
                        with open(user_data_file, 'w') as f:
                            json.dump(user_data, f, indent=4)
                        await event.respond("- تم حفظ كود الجلسة بنجاح .", buttons=[[Button.inline("‹ رجوع ›", data='back')]])
                    except (FileNotFoundError, json.JSONDecodeError):
                        await event.respond("حدث خطأ في تحديث بيانات المستخدم.", buttons=[[Button.inline("‹ رجوع ›", data='add_account')]])

            except Exception as e:
                await event.respond(f" كود الجلسة غير صالح, تحقق منه وحاول مرة اخرى", buttons=[[Button.inline("‹ رجوع ›", data='add_account')]])

        except asyncio.TimeoutError:
            await event.respond("- انتهى وقت الانتظار.", buttons=[[Button.inline("‹ رجوع ›", data='add_account')]])
        except Exception as e:
            await event.respond(f"حدث خطأ غير متوقع:  {e}", buttons=[[Button.inline("‹ رجوع ›", data='add_account')]])

async def CheckClient(session_code, event):
    client = TelegramClient(StringSession(session_code), api_id, api_hash)
    try:
        await client.connect()
        if not await client.is_user_authorized():
            await client.disconnect()
            return False
        else:
            await client.disconnect()
            return True
    except Exception as e:
        return False

async def handle_add_account_phone(event):
    user_id = event.sender_id
    user_data_file = 'users/' + str(user_id) + ".json"
    with open(user_data_file, 'r') as f:
        user_data = json.load(f)
    if user_data["session"] != "":
        await event.edit('```- لقد قمت باضافة حساب مسبقا .```', buttons=[[Button.inline('‹ حذف الحساب ›', 'delete_account'), Button.inline('‹ تغيير الحساب ›', 'change_Account')],[Button.inline('‹ رجوع ›', 'add')],])
        return
    async with client.conversation(event.sender_id, timeout=300) as conv:
        try:
            await event.delete()
            await conv.send_message("```- ارسل رقم الهاتف ❨ ارقام فقط و برمز الدوله ❩```\nللالغاء ارسل - ( /cancel ) .")
            phone_number = (await conv.get_response()).text
            if phone_number.lower() == "/cancel":
                await event.respond('- تم الغاء العملية .', buttons=[[Button.inline("‹ رجوع ›", data='add_account')]])
                return 
            if not phone_number.startswith('+') or not phone_number[1:].isdigit():
                await event.respond("رقم الهاتف غير صالح. يرجى إدخال رقم هاتف صحيح مع رمز الدولة (+).", buttons=[[Button.inline("‹ المحاولة مجددا ›", data='add_account')]])
                return
        except TimeoutError:
            await event.respond('انتهى الوقت لاضافة الحساب , حاول مجددا', buttons=[[Button.inline("‹ المحاولة مجددا ›", data='add_account')]])

        try:
            client_user = TelegramClient(StringSession(), api_id, api_hash) 
            await client_user.connect()
            if not client_user.is_connected():
                await event.respond("لا يمكن إرسال الطلبات أثناء عدم الاتصال", buttons=[[Button.inline("‹ المحاولة مجددا ›", data='add_account')]])
                return

            if not await client_user.is_user_authorized():
                await client_user.send_code_request(phone_number)

                try:
                    await conv.send_message("```- ارسل الكود المرسل للرقم من تطبيق Telegram •```\n``` ارسل الكود بهذا الشكل 1 2 3 4 5```\nللالغاء ارسل - ( /cancel ) .")
                    verification_code = (await conv.get_response()).text
                    verification_code = verification_code.replace(" ", "")
                    if verification_code.lower() == "/cancel":
                        await event.respond('- تم الغاء العملية .', buttons=[[Button.inline("‹ رجوع ›", data='add_account')]])
                        return 

                    if not verification_code.isdigit():
                        await conv.send_message("رمز التحقق غير صالح. يرجى إدخال رمز صحيح.", buttons=[[Button.inline("‹ المحاولة مجددا ›", data='add_account')]])
                        return

                    await client_user.sign_in(phone_number, verification_code)
                except TimeoutError:
                    await event.respond('انتهى الوقت لارسال رمز التحقق , حاول مجددا', buttons=[[Button.inline("‹ المحاولة مجددا ›", data='add_account')]])
                    return
                except SessionPasswordNeededError:
                    try:
                        await conv.send_message("```- ارسل باسورد التحقق بخطوتين •```\nللالغاء ارسل - ( /cancel ) .")
                        password = (await conv.get_response()).text
                        if password.lower() == "/cancel":
                            await event.respond('- تم الغاء العملية .', buttons=[[Button.inline("‹ رجوع ›", data='add_account')]])
                            return 
                        await client_user.sign_in(password=password)
                    except TimeoutError:
                        await event.respond('انتهى الوقت لارسال باسورد التحقق , حاول مجددا', buttons=[[Button.inline("‹ المحاولة مجددا  ›", data='add_account')]])
                        return
                    except:
                        await event.respond('الباسورد خاطئ , حاول مجددا', buttons=[[Button.inline("‹ المحاولة مجددا ›", data='add_account')]])
                        return
            session = client_user.session.save()

            await conv.send_message("```✅︙تم تاكيد الرقم بنجاح •```", buttons=[[Button.inline("‹ رجوع ›", data='add_account')]])

            with open(user_data_file, 'r') as f:
                user_data = json.load(f)
            user_data["session"] = session
            
            with open(user_data_file, 'w') as f:
                json.dump(user_data, f, indent=4)

        except ValueError:
            await conv.send_message("API ID أو API HASH غير صالح. يرجى التحقق والمحاولة مرة أخرى.", buttons=[[Button.inline("‹ المحاولة مجددا ›", data='add_account')]])
            return
        except Exception as e:
            await conv.send_message(f"حدث خطأ: {str(e)}", buttons=[[Button.inline("‹ رجوع ›", data='add_account')]])
            return
        finally:
            if client_user and client_user.is_connected():
                await client_user.disconnect()


async def handle_start(event):
    user_id = event.sender_id
    user_data_file = 'users/' + str(user_id) + ".json"
    user_data = load_user_data(user_data_file)
    first_name = event.sender.first_name
    last_name = event.sender.last_name
    full_name = f"{first_name} {last_name}" if last_name else first_name
    tip_status = user_data.get("tip", {"status": False})["status"]
    salary_status = user_data.get("salary", {"status": False})["status"]

    buttons = [
        [Button.inline('‹ الإضافات ›', data=b'add')],
        [Button.inline(f"‹ {'إيقاف' if tip_status else 'تفعيل'} البخشيش ›", data=b'tip' if not tip_status else b'tip_off'), Button.inline(f"‹ {'إيقاف' if salary_status else 'تفعيل'} الراتب ›", data=b'salary' if not salary_status else b'salary_off')],
        [Button.inline("‹ الاستثمار ›", data=b'invest')],
        [Button.inline("‹ ايقاف التجميع ›", data=b'off_collect'), Button.inline("‹ بدء التجميع ›", data=b'on_collect')],
        [Button.inline("‹ معلومات حسابك البنكي ›", data=b'bank_information')],
        [Button.inline('‹ تحويل فلوس ›', 'transfer_amounts'), Button.inline('‹ توب الفلوس ›', 'money_top')],
        [Button.url("‹ Developer ›", url='t.me/MM_GM')],
        [Button.url(" 🖥 ", url='t.me/xDythonBot/WaD')],
    ]
    await event.respond(f"""
- اهلا : [ {full_name} ](tg://settings) .
- البوت مخصص لتجميع فلوس من بوت وعد 🧚 .
-  البوت امن , ولكن لاينصح باستخدام حساب رسمي حفاظأً على بياناتك!""", buttons=buttons)



async def handle_tip(event):
    await toggle_feature(event, "tip")

async def handle_salary(event):
    await toggle_feature(event, "salary")

async def handle_tip_off(event):
    await toggle_feature(event, "tip", False)

async def handle_salary_off(event):
    await toggle_feature(event, "salary", False)

async def toggle_feature(event, feature_name, turn_on=True):
    user_id = event.sender_id
    user_data_file = 'users/' + str(user_id) + ".json"
    user_data = load_user_data(user_data_file)

    user_data[feature_name] = {"status": turn_on}
    save_user_data(user_data, user_data_file)
    await update_buttons(event)

async def update_buttons(event):
    user_id = event.sender_id
    user_data_file = 'users/' + str(user_id) + ".json"
    user_data = load_user_data(user_data_file)
    first_name = event.sender.first_name
    last_name = event.sender.last_name
    full_name = f"{first_name} {last_name}" if last_name else first_name
    tip_status = user_data.get("tip", {"status": False})["status"]
    salary_status = user_data.get("salary", {"status": False})["status"]

    buttons = [
        [Button.inline('‹ الإضافات ›', data=b'add')],
        [Button.inline(f"‹ {'إيقاف ' if tip_status else 'تفعيل'} البخشيش ›", data=b'tip' if not tip_status else b'tip_off'), Button.inline(f"‹ {'إيقاف' if salary_status else 'تفعيل'} الراتب ›", data=b'salary' if not salary_status else b'salary_off')],
        [Button.inline("‹ الاستثمار ›", data=b'invest')],
        [Button.inline("‹ ايقاف التجميع ›", data=b'off_collect'), Button.inline("‹ بدء التجميع ›", data=b'on_collect')],
        [Button.inline("‹ معلومات حسابك البنكي ›", data=b'bank_information')],
        [Button.inline('‹ تحويل فلوس ›', 'transfer_amounts'), Button.inline('‹ توب الفلوس ›', 'money_top')],
        [Button.url("‹ Developer ›", url='t.me/MM_GM')],
        [Button.url(" 🖥 ", url='t.me/xDythonBot/WaD')],

    ]
    await event.edit(f"""
- اهلا : [ {full_name} ](tg://settings) .
- البوت مخصص لتجميع فلوس من بوت وعد 🧚 .
-  البوت امن , ولكن لاينصح باستخدام حساب رسمي حفاظأً على بياناتك!""", buttons=buttons)

def load_user_data(user_data_file):
    try:
        with open(user_data_file, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_user_data(user_data, user_data_file):
    with open(user_data_file, 'w') as f:
        json.dump(user_data, f, indent=4)

async def handle_invest(event):
    user_id = event.sender_id
    user_data_file = 'users/' + str(user_id) + ".json"
    with open(user_data_file, 'r') as f:
        user_data = json.load(f)

    message = """
    ``` - استثمار تلقائي : يتم استثمار جميع الاموال بحسابك تلقائيا ```

    ``` - استثمار محدد : يتم استثمار عدد معين من الاموال التي ستقوم بتحديدها ```

    ``` - حذف الاستثمار : يتم حذف جميع قيم الاستثمار التي اخترتها ويتم ايقاف الاستثمار التلقائي ```

    """

    if not user_data["invest"]["status"]:
        await event.edit(message, buttons=[
        [Button.inline('‹ حذف الاستثمار ›', data=b'delete_invest')],       
        [Button.inline('‹ استثمار محدد ›', data=b'set_invest'), Button.inline('‹ تفعيل استثمار تلقائي ›', data=b'auto_invest_on')],
        [Button.inline('‹ رجوع ›', data=b'back')],     
        ])
        return
    elif user_data["invest"]["status"]:
        await event.edit(message, buttons=[
        [Button.inline('‹ حذف الاستثمار ›', data=b'delete_invest')],       
        [Button.inline('‹ استثمار محدد ›', data=b'set_invest'), Button.inline('‹ تعطيل استثمار تلقائي ›', data=b'auto_invest_off')],
        [Button.inline('‹ رجوع ›', data=b'back')],     
        ])

async def handle_set_invest(event):
    user_id = event.sender_id
    user_data_file = 'users/' + str(user_id) + ".json"
    async with client.conversation(event.chat_id) as conv:
        try:
            with open(user_data_file, 'r') as f:
                user_data = json.load(f)

            await event.edit('```- ادخل قيمة الاستثمار :```\nللالغاء ارسل - ( /cancel ) .')
            new_investment_value = await conv.wait_event(events.NewMessage(from_users=event.sender_id))
            new_investment_value = new_investment_value.text
            if new_investment_value.lower() == "/cancel":
                await event.respond('- تم الغاء العملية .', buttons=[[Button.inline("‹ رجوع ›", data='invest')]])
                return 
            try:
                new_investment_value = int(new_investment_value)

            except ValueError:
                await event.respond('- عليك ارسال المبلغ بشكل رقم !', buttons=[[Button.inline("‹ المحاولة مجددا ›", data='invest')]])
                return
            if new_investment_value < 200:
                await event.respond('- الحد الادنى للاستثمار 200 :', buttons=[Button.inline('‹ المحاولة مجددا ›', data=b'invest')])
                return
            user_data["invest"]["value"] = new_investment_value
            user_data["invest"]["status"] = False

            with open(user_data_file, 'w') as f:
                json.dump(user_data, f, indent=4)

            await event.respond('- تم تعيين قيمة الاستثمار بنجاح .', buttons=[[Button.inline("‹ رجوع ›", data='invest')]])

        except (FileNotFoundError, json.JSONDecodeError, ValueError, TypeError) as e:
            await event.respond(f"حدث خطأ: {e}", buttons=[[Button.inline("‹ رجوع ›", data='invest')]])
        except Exception as e:
            await event.respond(f"حدث خطأ غير متوقع: {e}", buttons=[[Button.inline("‹ رجوع ›", data='invest')]])

async def load_user_datas(user_id):
    """Load user data from a JSON file."""
    user_data_file = f"users/{user_id}.json"
    try:
        with open(user_data_file, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise e

async def handle_auto_invest_on(event):
    user_id = event.sender_id
    user_data_file = f"users/{user_id}.json"
    user_data = await load_user_datas(user_id)
    user_data["invest"]["status"] = True
    with open(user_data_file, 'w') as f:
        json.dump(user_data, f, indent=4)
    await handle_invest(event)

async def handle_auto_invest_off(event):
    user_id = event.sender_id
    user_data_file = f"users/{user_id}.json"
    user_data = await load_user_datas(user_id)
    user_data["invest"]["status"] = False
    with open(user_data_file, 'w') as f:
        json.dump(user_data, f, indent=4)
    await handle_invest(event)

async def handle_delete_invest(event):
    user_id = event.sender_id
    user_data_file = 'users/' + str(user_id) + ".json"

    try:
        with open(user_data_file, 'r') as f:
            user_data = json.load(f)
        if user_data["invest"]["status"] == False:
            if user_data["invest"]["value"] == 0:
                await event.edit('```- بيانات الاستثمار محذوفة بالفعل .```', buttons=[Button.inline('‹ رجوع ›', 'invest')])
                return

        user_data["invest"]["value"] = 0
        user_data["invest"]["status"] = False

        with open(user_data_file, 'w') as f:
            json.dump(user_data, f, indent=4)

        await event.edit('- تم حذف بيانات الاستثمار .', buttons=[Button.inline('‹ رجوع ›', 'invest')])

    except (FileNotFoundError, json.JSONDecodeError) as e:
        await event.respond(f"- حدث خطأ: {e}", buttons=[[Button.inline("‹ رجوع ›", data='invest')]])

async def initialize_client(event, session_code):
    try:
        user_client = TelegramClient(StringSession(session_code), api_id, api_hash)
        await user_client.connect()
        return user_client
    except Exception as e:
        await event.respond(f'- يوجد مشكلة بالاتصال بالخادم, {e} .', buttons=[[Button.inline("‹ رجوع ›", data='invest')]])
        return None

class CollectHandler:
    def __init__(self):
        self.task_manager = None
        self.collection_task = None
    async def handle_off_collect(self, event):
        """Handle turning off the collect feature"""
        user_id = event.sender_id
        user_data_file = f"users/{user_id}.json"
        
        try:
            with open(user_data_file, 'r', encoding='utf-8') as f:
                user_data = json.load(f)
        except FileNotFoundError:
            await event.edit(
                '- ملف المستخدم غير موجود .', 
                buttons=[Button.inline("‹ رجوع ›", data='back')]
            )
            return
        except json.JSONDecodeError:
            await event.edit(
                '- خطأ في قراءة ملف المستخدم .', 
                buttons=[Button.inline("‹ رجوع ›", data='back')]
            )
            return

        if not user_data.get("session"):
            await event.edit(
                '- لم تقم باضافة حساب .', 
                buttons=[Button.inline("‹ رجوع ›", data='back')]
            )
            return

        if not user_data.get("collect_status", False):
            await event.edit(
                '- التجميع متوقف بالفعل .', 
                buttons=[Button.inline("‹ رجوع ›", data='back')]
            )
            return

        user_data["collect_status"] = False
        
        try:
            with open(user_data_file, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=4)
        except Exception as e:
            await event.edit(
                f'- خطأ في حفظ البيانات: {str(e)}', 
                buttons=[Button.inline("‹ رجوع ›", data='back')]
            )
            return

        if hasattr(self, 'task_manager') and self.task_manager:
            await self.task_manager.stop_all_tasks()
            self.task_manager = None

        await event.edit(
            "- تم ايقاف التجميع .", 
            buttons=[Button.inline("‹ رجوع ›", data='back')]
        )

    async def handle_on_collect(self, event):
        """Handle the collect button click event"""
        user_id = event.sender_id
        user_data_file = f"users/{user_id}.json"
        
        try:
            with open(user_data_file, 'r', encoding='utf-8') as f:
                user_data = json.load(f)
        except FileNotFoundError:
            await event.edit(
                '- ملف المستخدم غير موجود .', 
                buttons=[Button.inline("‹ رجوع ›", data='back')]
            )
            return
        except json.JSONDecodeError:
            await event.edit(
                '- خطأ في قراءة ملف المستخدم .', 
                buttons=[Button.inline("‹ رجوع ›", data='back')]
            )
            return

        if user_data.get("collect_status", False):
            await event.edit(
                '- التجميع يعمل بالفعل .', 
                buttons=[Button.inline("‹ رجوع ›", data='back')]
            )
            return

        try:
            session = user_data.get('session')
            if not session:
                await event.edit(
                    '- لم تقم باضافة حساب .', 
                    buttons=[Button.inline("‹ رجوع ›", data='back')]
                )
                return
                
            user_client = TelegramClient(StringSession(session), api_id, api_hash)
            await user_client.connect()
            
            if not await user_client.is_user_authorized():
                await event.edit(
                    '- انتهت صلاحية الجلسة، قم باضافة الحساب مرة اخرى .', 
                    buttons=[Button.inline("‹ رجوع ›", data='back')]
                )
                return

        except Exception as e:
            await event.edit(
                f'- خطأ في تسجيل الدخول: {str(e)}', 
                buttons=[Button.inline("‹ رجوع ›", data='back')]
            )
            return

        try:
            group_id = user_data.get("added_group")
            if not group_id:
                await event.edit(
                    '- لم تقم باضافة قناة التجميع .', 
                    buttons=[Button.inline("‹ رجوع ›", data='back')]
                )
                await user_client.disconnect()
                return
                
            group_entity = await user_client.get_entity(int(group_id))
            
        except Exception as e:
            await event.edit(
                f'- خطأ في الوصول للمجموعة: {str(e)}',
                buttons=[Button.inline("‹ رجوع ›", data='back')]
            )
            await user_client.disconnect()
            return

        user_data["collect_status"] = True
        with open(user_data_file, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=4)

        try:
            self.task_manager = TaskManager(user_client, group_entity, user_data_file)
            await self.task_manager.start_loops()
            
            await event.edit(
                '- تم تفعيل التجميع .', 
                buttons=[Button.inline("‹ رجوع ›", data='back')]
            )
        except Exception as e:
            await event.edit(
                f'- خطأ في بدء التجميع: {str(e)}',
                buttons=[Button.inline("‹ رجوع ›", data='back')]
            )
            await user_client.disconnect()
            user_data["collect_status"] = False
            with open(user_data_file, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=4)


collect_handler = CollectHandler()


class TaskManager:
    def __init__(self, user_client, group_entity, user_data_file):
        self.user_client = user_client
        self.group_entity = group_entity
        self.user_data_file = user_data_file
        self.running = True
        self.tasks = {
            'salary': None,
            'tip': None,
            'invest': None
        }
        self.task_delays = {
            'salary': 610,
            'tip': 620,
            'invest': 15
        }
        self.last_run_times = {
            'salary': 0,
            'tip': 0,
            'invest': 0
        }

        self.user_data = self.load_user_dataer()

    def load_user_dataer(self):
        """تحميل بيانات المستخدم من الملف"""
        try:
            with open(self.user_data_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"خطأ في قراءة ملف البيانات: {e}")
            return {}

    async def start_loops(self):
        """Start all collection tasks using a single loop."""
        try:
            while self.running:
                current_time = time.time()
                for task_name, task_func in self.get_task_functions().items():
                    if not self.check_task_status(task_name):
                        continue
                    
                    if current_time - self.last_run_times[task_name] >= self.task_delays[task_name]:
                        try:
                            await task_func()
                            self.last_run_times[task_name] = current_time
                        except Exception as e:
                            print(f"Error in task {task_name}: {e}")
        except Exception as e:
            print(f"Error in main loop: {e}")

    def check_task_status(self, task_name):
        """التحقق من حالة المهمة في user_data"""
        try:
            data_key = 'tip' if task_name == 'tip' else task_name
            
            if (data_key in self.user_data and 
                'status' in self.user_data[data_key] and 
                self.user_data[data_key]['status']):
                return True
            return False
        except Exception as e:
            print(f"خطأ في التحقق من حالة {task_name}: {e}")
            return False

    def get_task_functions(self):
        """Return a dictionary of task functions."""
        return {
            'salary': self.send_salary_status,
            'tip': self.send_tip_status,
            'invest': lambda: self.send_invest_status(3)
        }

    async def send_salary_status(self):
        await self.user_client.send_message(self.group_entity, "راتب")


    async def send_tip_status(self):
        await self.user_client.send_message(self.group_entity, "بخشيش")        


    async def send_invest_status(self, value):
        try:
            sent_message = await self.user_client.send_message(self.group_entity, "فلوس")
            start_time = time.time()
            timeout = 10 
        
            while time.time() - start_time < timeout:
                async for message in self.user_client.iter_messages(
                    self.group_entity,
                    min_id=sent_message.id,
                ):
                    if "فلوسك" in message.text:
                        try:
                            amount = message.text.split(" ")[2]
                            await self.user_client.send_message(
                                self.group_entity,
                                f"استثمار {amount}"
                            )

                            return
                        except:
                            print("Could not extract amount from message")
                            return

        except Exception as e:
            print(f"Error in send_invest_status: {e}")

    async def stop_all_tasks(self):
        """Stop all running tasks"""
        self.running = False
        for task_name, task in self.tasks.items():
            if task and not task.cancelled():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
                self.tasks[task_name] = None


async def bank_information(event):
    user_id = event.sender_id
    user_data_file = f"users/{user_id}.json"

    try:
        with open(user_data_file, 'r') as f:
            user_data = json.load(f)
    except FileNotFoundError:
        await event.respond('- ملف المستخدم غير موجود .', buttons=[[Button.inline("‹ رجوع ›", data='back')]])
        return
    except json.JSONDecodeError:
        await event.respond('يوجد مشكلة في قراءة ملف البيانات.')
        return

    session_code = user_data.get("session", '')
    if not session_code:
        await event.edit('```- لم تقم باضافة حساب .```', buttons=[Button.inline('‹ رجوع ›', 'back')])
        return

    group_id = user_data.get("added_group", '')
    if not group_id:
        await event.edit('```- لم تقم باضافة مجموعة .```', buttons=[Button.inline('‹ رجوع ›', 'back')])
        return

    user_client = await initialize_client(event, session_code)
    await event.edit('```- جاري جلب المعلومات .```')
    await asyncio.sleep(1.7)
    await event.edit('```- جاري جلب المعلومات ..```')
    await asyncio.sleep(1.7)
    await event.edit('```- جاري جلب المعلومات ...```')
    await asyncio.sleep(1.7)
    group_id = int(group_id)
    group_entity = await user_client.get_entity(group_id)

    bot = await user_client.get_entity('@d7bot') 
    message = await get_information_message(user_client, group_entity, bot, event)
    await event.edit(message, buttons=[Button.inline('‹ رجوع ›', 'back')])

async def get_information_message(user_client, group_entity, bot, event):
    async with user_client.conversation(group_entity) as conv:
        try:
            sent_message = await user_client.send_message(group_entity, 'حسابي') 
            response = await conv.wait_event(events.NewMessage(chats=group_entity, from_users=bot, pattern=r"^⇜ الاسم"), timeout=10)
            if response and "ريال" in response.message.text:
                message = (f"**المعلومات الخاصة بحسابك **:\n\n{response.message.text}")
                return message
            else:
                return "غير صالح"
        except TimeoutError:
            return {}
    
async def delete_account(event):
    user_id = event.sender_id
    user_data_file = f"users/{user_id}.json"

    try:
        with open(user_data_file, 'r') as f:
            user_data = json.load(f)
        user_data["session"] = ""
        with open(user_data_file, 'w') as f:
            json.dump(user_data, f, indent=4)
        await event.edit('- تم حذف الحساب بنجاح .',buttons=[Button.inline('‹ رجوع ›', 'add_account')])
    except Exception as e:
        await event.edit(f'- حدث خطا : {e}',buttons=[Button.inline('‹ رجوع ›', 'add_account')])

async def change_Account(event):
    await event.edit("""
        - لديك طريقتين لتغيير حسابك في البوت !
        ```االطريقة الاولى : عن طريق رقم الهاتف سيتم طلب كود التسجيل الى حسابك \n سيتم طلب رمز التحقق بخطوتين ان وجد```
 
        ``` الطريقة الثانية : عن طريق كود جلسة التليثون ( السيشن ) ``` """, buttons=[
            [Button.inline('‹ استخدام سيشن جلسة ›', data=b'convert_Session'), Button.inline('‹ استخدام رقم الهاتف ›', data=b'convert_phone')],
            [Button.inline('‹ رجوع ›', 'add_account')]
        ])

async def handle_convert_session(event):
    async with client.conversation(event.chat_id) as conv:
        user_id = event.sender_id
        user_data_file = 'users/' + str(user_id) + ".json"
        with open(user_data_file, 'r') as f:
            user_data = json.load(f)
        try:
            await event.edit("""
            ```- أرسل كود الجلسة ( السيشن ) الخاص بحساب التليكرام ! ```
            - للألغاء ارسل ( /cancel ) .""")

            message = await conv.wait_event(events.NewMessage(
                from_users=event.sender_id, chats=event.chat_id
            ), timeout=30)

            session_code = message.text.strip()
            if session_code.lower() == "/cancel":
                await event.respond('- تم الغاء العملية .', buttons=[[Button.inline("‹ رجوع ›", data='add_account')]])
                return
            try:
                await CheckClient(session_code, event)
                if CheckClient:
                    try:
                        with open(user_data_file, 'r') as f:
                            user_data = json.load(f)
                        user_data["session"] = session_code
                        with open(user_data_file, 'w') as f:
                            json.dump(user_data, f, indent=4)
                        await event.respond("- تم حفظ كود الجلسة بنجاح .", buttons=[[Button.inline("‹ رجوع ›", data='back')]])
                    except (FileNotFoundError, json.JSONDecodeError):
                        await event.respond("حدث خطأ في تحديث بيانات المستخدم.", buttons=[[Button.inline("‹ رجوع ›", data='add_account')]])

            except Exception as e:
                await event.respond(f" كود الجلسة غير صالح, تحقق منه وحاول مرة اخرى", buttons=[[Button.inline("‹ رجوع ›", data='add_account')]])

        except asyncio.TimeoutError:
            await event.respond("- انتهى وقت الانتظار.", buttons=[[Button.inline("‹ رجوع ›", data='add_account')]])
        except Exception as e:
            await event.respond(f"حدث خطأ غير متوقع:  {e}", buttons=[[Button.inline("‹ رجوع ›", data='add_account')]])

async def handle_convert_phone(event):
    user_id = event.sender_id
    user_data_file = 'users/' + str(user_id) + ".json"
    async with client.conversation(event.sender_id, timeout=300) as conv:
        try:
            await event.delete()
            await conv.send_message("```- ارسل رقم الهاتف ❨ ارقام فقط و برمز الدوله ❩```\nللالغاء ارسل - ( /cancel ) .")
            phone_number = (await conv.get_response()).text
            if phone_number.lower() == "/cancel":
                await event.respond('- تم الغاء العملية .', buttons=[[Button.inline("‹ رجوع ›", data='add_account')]])
                return 
            if not phone_number.startswith('+') or not phone_number[1:].isdigit():
                await event.respond("رقم الهاتف غير صالح. يرجى إدخال رقم هاتف صحيح مع رمز الدولة (+).", buttons=[[Button.inline("‹ المحاولة مجددا ›", data='add_account')]])
                return
        except TimeoutError:
            await event.respond('انتهى الوقت لاضافة الحساب , حاول مجددا', buttons=[[Button.inline("‹ المحاولة مجددا ›", data='add_account')]])

        try:
            client_user = TelegramClient(StringSession(), api_id, api_hash) 
            await client_user.connect()
            if not client_user.is_connected():
                await event.respond("لا يمكن إرسال الطلبات أثناء عدم الاتصال", buttons=[[Button.inline("‹ المحاولة مجددا ›", data='add_account')]])
                return

            if not await client_user.is_user_authorized():
                await client_user.send_code_request(phone_number)

                try:
                    await conv.send_message("```- ارسل الكود المرسل للرقم من تطبيق Telegram •```\n``` ارسل الكود بهذا الشكل 1 2 3 4 5```\nللالغاء ارسل - ( /cancel ) .")
                    verification_code = (await conv.get_response()).text
                    verification_code = verification_code.replace(" ", "")
                    if verification_code.lower() == "/cancel":
                        await event.respond('- تم الغاء العملية .', buttons=[[Button.inline("‹ رجوع ›", data='add_account')]])
                        return 

                    if not verification_code.isdigit():
                        await conv.send_message("رمز التحقق غير صالح. يرجى إدخال رمز صحيح.", buttons=[[Button.inline("‹ المحاولة مجددا ›", data='add_account')]])
                        return

                    await client_user.sign_in(phone_number, verification_code)
                except TimeoutError:
                    await event.respond('انتهى الوقت لارسال رمز التحقق , حاول مجددا', buttons=[[Button.inline("‹ المحاولة مجددا ›", data='add_account')]])
                    return
                except SessionPasswordNeededError:
                    try:
                        await conv.send_message("```- ارسل باسورد التحقق بخطوتين •```\nللالغاء ارسل - ( /cancel ) .")
                        password = (await conv.get_response()).text
                        if password.lower() == "/cancel":
                            await event.respond('- تم الغاء العملية .', buttons=[[Button.inline("‹ رجوع ›", data='add_account')]])
                            return 
                        await client_user.sign_in(password=password)
                    except TimeoutError:
                        await event.respond('انتهى الوقت لارسال باسورد التحقق , حاول مجددا', buttons=[[Button.inline("‹ المحاولة مجددا  ›", data='add_account')]])
                        return
                    except:
                        await event.respond('الباسورد خاطئ , حاول مجددا', buttons=[[Button.inline("‹ المحاولة مجددا ›", data='add_account')]])
                        return
            session = client_user.session.save()

            await conv.send_message("```✅︙تم تاكيد الرقم بنجاح •```", buttons=[[Button.inline("‹ رجوع ›", data='add_account')]])

            with open(user_data_file, 'r') as f:
                user_data = json.load(f)
            user_data["session"] = session
            
            with open(user_data_file, 'w') as f:
                json.dump(user_data, f, indent=4)

        except ValueError:
            await conv.send_message("API ID أو API HASH غير صالح. يرجى التحقق والمحاولة مرة أخرى.", buttons=[[Button.inline("‹ المحاولة مجددا ›", data='add_account')]])

        except Exception as e:
            await conv.send_message(f"حدث خطأ: {str(e)}", buttons=[[Button.inline("‹ رجوع ›", data='add_account')]])

        finally:
            if client_user and client_user.is_connected():
                await client_user.disconnect()

async def money_top(event):
    await asyncio.sleep(4)
    user_id = event.sender_id
    user_data_file = f"users/{user_id}.json"

    try:
        with open(user_data_file, 'r') as f:
            user_data = json.load(f)
    except FileNotFoundError:
        await event.respond('- ملف المستخدم غير موجود .', buttons=[[Button.inline("‹ رجوع ›", data='back')]])
        return
    except json.JSONDecodeError:
        await event.respond('يوجد مشكلة في قراءة ملف البيانات.')
        return

    session_code = user_data.get("session", '')
    if not session_code:
        await event.edit('```- لم تقم باضافة حساب .```', buttons=[Button.inline('‹ رجوع ›', 'back')])
        return

    group_id = user_data.get("added_group", '')
    if not group_id:
        await event.edit('```- لم تقم باضافة مجموعة .```', buttons=[Button.inline('‹ رجوع ›', 'back')])
        return
    user_client = await initialize_client(event, session_code)  
    await event.edit('```- جاري جلب المعلومات .```')
    await asyncio.sleep(1.7)
    await event.edit('```- جاري جلب المعلومات ..```')
    await asyncio.sleep(1.7)
    await event.edit('```- جاري جلب المعلومات ...```')
    await asyncio.sleep(1.7)
    group_id = int(group_id)
    group_entity = await user_client.get_entity(group_id)

    bot = await user_client.get_entity('@d7bot')
    message = await get_information_msg(user_client, group_entity, bot)
    
    await event.edit(message, buttons=[Button.inline('‹ رجوع ›', 'back')])

async def get_information_msg(user_client, group_entity, bot):
    async with user_client.conversation(group_entity) as conv:
        try:
            sent_message = await user_client.send_message(group_entity, 'توب الفلوس')
            response = await conv.wait_event(events.NewMessage(chats=group_entity, from_users=bot, pattern=r"^توب"), timeout=10)
            if response and "توب" in response.message.text:
                message = response.message.text
                return message
            else:
                return "غير صالح"
        except asyncio.TimeoutError:
            return "مشكلة في asyncio"
        except Exception as e:
            return f'حدث خطأ: {str(e)}'

async def transfer_amounts(event):
    user_id = event.sender_id
    user_data_file = f"users/{user_id}.json"

    try:
        with open(user_data_file, 'r') as f:
            user_data = json.load(f)
    except FileNotFoundError:
        await event.respond('- ملف المستخدم غير موجود .', buttons=[[Button.inline("‹ رجوع ›", data='back')]])
        return
    except json.JSONDecodeError:
        await event.respond('يوجد مشكلة في قراءة ملف البيانات.')
        return

    session_code = user_data.get("session", '')
    if not session_code:
        await event.edit('```- لم تقم باضافة حساب .```', buttons=[Button.inline('‹ رجوع ›', 'back')])
        return

    group_id = user_data.get("added_group", '')
    if not group_id:
        await event.edit('```- لم تقم باضافة مجموعة .```', buttons=[Button.inline('‹ رجوع ›', 'back')])
        return
    await event.edit('```- جاري جلب المعلومات .```')
    await event.edit('```- جاري جلب المعلومات ..```')    
    await event.edit('```- جاري جلب المعلومات ...```')
    user_client = await initialize_client(event, session_code)
    group_id = int(group_id)
    group_entity = await user_client.get_entity(group_id)
    bot = await user_client.get_entity('@d7bot')     
    await asyncio.sleep(1)
    message = await get_information_message(user_client, group_entity, bot, event)
    match = re.search(r'الرصيد ↢ \(\s*(\d+)\s*ريال', message)
    if not match:
        return "PROBLEM"
    if match:
        your_money = match.group(1)
        your_money = int(your_money)

    async with client.conversation(event.chat_id) as conv:
        await event.delete()
        await conv.send_message(f'```- ارسل الكمية التي تود تحويلها :\nرصيدك الحالي : {your_money} ريال```')
        amount = (await conv.get_response()).text
        try:
            amount = int(amount)
        except ValueError:
            await event.respond('- يرجى ارسال كمية صالحة .', buttons=[Button.inline('‹ المحاولة مجددا ›', 'back')])
            return
        if amount > your_money:
            await event.respond('- رصيدك غير كافي .', buttons=[Button.inline('‹ المحاولة مجددا ›', 'back')])
            return
        if amount < 200:
            await event.respond('- الحد الادنى للتحويل 200 ريال .', buttons=[Button.inline('‹ المحاولة مجددا ›', 'back')])
            return
        await conv.send_message('```- ارسل رقم الحساب البنكي الذي تود التحويل له :```')
        bank_id = (await conv.get_response()).text

        await transfer_procesess(amount, bank_id, user_client, bot, group_entity, event)

async def transfer_procesess(amount, bank_id, user_client, bot, group_entity, event):
    async with user_client.conversation(group_entity) as conv:
        try:
            await user_client.send_message(group_entity, f'تحويل {amount}')
            await asyncio.sleep(5)
            sent_message = await user_client.send_message(group_entity, f'{bank_id}')
            response = await conv.wait_event(events.NewMessage(chats=group_entity, from_users=bot), timeout=30)
            if response.reply_to_msg_id == sent_message.id and "مافي حساب بهذا الرقم" in response.text:
                await event.respond('- الحساب غير صحيح .', buttons=[Button.inline('‹ المحاولة مجددا ›', 'back')])
            elif response.reply_to_msg_id == sent_message.id and "تحول لنفسك ي اثول" in response.text:
                await event.respond('- لاتستطيع تحوبل الاموال لنفسك .', buttons=[Button.inline('‹ المحاولة مجددا ›', 'back')])
            elif response.reply_to_msg_id == sent_message.id and "حوالة صادرة" in response.text:
                await event.respond(f'- تم التحويل بنجاح وخصم {amount} من حسابك .', buttons=[Button.inline('‹ رجوع ›', 'back')])
        except TimeoutError:
            await event.respond('- لم يتم الاستجابة من بوت وعد .', buttons=[Button.inline('‹ المحاولة مجددا ›', 'back')])
            return

async def check_block(event):
    sender_id = event.sender_id
    is_blocked = sender_id in blocked_users
    if is_blocked:
        await event.edit("- انت محظور من البوت ولاتستطيع استخدامه .\n- لفك الحظر راسل المطور .", buttons=[Button.url('‹ Developer ›', 't.me/MM_GM')])
        return True
    return False

async def main():
    await client.start(bot_token=bot_token)
    print('Bot started.')
    await client.run_until_disconnected()   

asyncio.run(main())
