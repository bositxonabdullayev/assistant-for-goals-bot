from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from tools_tasks import t_add, t_list, t_move, t_done
from tools_money import add_tx, report_current_month

router = Router()

def setup_handlers(dp):
    dp.include_router(router)

@router.message(CommandStart())
async def start(m: Message):
    await m.answer(
        "Assalomu alaykum! Men agent-botman. Qisqa va aniq yordam beraman.\n"
        "Misollar:\n"
        "- /tadd Kofe olish\n- /tlist\n- /addexp 12000 \"Kofe\" Kafe\n- /rep"
    )

# Tasks
@router.message(Command('tadd'))
async def cmd_tadd(m: Message):
    title = m.text.partition(" ")[2].strip()
    if not title:
        return await m.answer("Format: /tadd Vazifa matni")
    r = t_add(m.from_user.id, title, None, None, "Today")
    await m.answer(f"✅ Task qo'shildi (id={r['task_id']}): {title}")

@router.message(Command('tlist'))
async def cmd_tlist(m: Message):
    data = t_list(m.from_user.id)
    if not data:
        return await m.answer("Bo'sh.")
    lines = []
    for col in data:
        lines.append(f"**{col['column']}**")
        for it in col['items']:
            lines.append(f"\u2022 #{it['id']} {it['title']}  {it['due'] or ''}")
    await m.answer("\n".join(lines), parse_mode="Markdown")

@router.message(Command('tmove'))
async def cmd_tmove(m: Message):
    parts = m.text.split(maxsplit=2)
    if len(parts)<3:
        return await m.answer("Format: /tmove <id> <Column>")
    try:
        tid = int(parts[1])
    except:
        return await m.answer("ID butun son bo'lishi kerak")
    r = t_move(m.from_user.id, tid, parts[2])
    await m.answer("✅ Ko'chirildi." if r.get("ok") else f"Xato: {r.get('error')}")

@router.message(Command('tdone'))
async def cmd_tdone(m: Message):
    parts = m.text.split(maxsplit=1)
    if len(parts)<2:
        return await m.answer("Format: /tdone <id>")
    try:
        tid = int(parts[1])
    except:
        return await m.answer("ID butun son bo'lishi kerak")
    r = t_done(m.from_user.id, tid)
    await m.answer("✅ Done." if r.get("ok") else f"Xato: {r.get('error')}")

# Money
@router.message(Command('addexp'))
async def cmd_addexp(m: Message):
    parts = m.text.split(" ", 1)
    if len(parts)<2:
        return await m.answer('Format: /addexp 12000 "Kofe" Kafe')
    rest = parts[1].strip()
    try:
        amount_str = rest.split(" ",1)[0]
        rest2 = rest[len(amount_str):].strip()
        note = rest2.split('"')[1]
        tail = rest2.split('"',2)[2].strip()
        category = tail or None
    except Exception:
        return await m.answer('Format: /addexp 12000 "Kofe" Kafe')
    r = add_tx(m.from_user.id, amount_str, "expense", category, note, None)
    await m.answer("✅ Xarajat qo'shildi." if r.get("ok") else "Xato.")

@router.message(Command('addin'))
async def cmd_addin(m: Message):
    parts = m.text.split(" ", 1)
    if len(parts)<2:
        return await m.answer('Format: /addin 300000 "Freelance" Ish')
    rest = parts[1].strip()
    try:
        amount_str = rest.split(" ",1)[0]
        rest2 = rest[len(amount_str):].strip()
        note = rest2.split('"')[1]
        tail = rest2.split('"',2)[2].strip()
        category = tail or None
    except Exception:
        return await m.answer('Format: /addin 300000 "Freelance" Ish')
    r = add_tx(m.from_user.id, amount_str, "income", category, note, None)
    await m.answer("✅ Daromad qo'shildi." if r.get("ok") else "Xato.")

@router.message(Command('rep'))
async def cmd_rep(m: Message):
    data = report_current_month(m.from_user.id)
    if not data:
        return await m.answer("Hisobot yo'q.")
    lines = ["**Joriy oy hisobot:**"]
    for row in data:
        lines.append(f"{row['type'][:3].upper()}  {row['category']}: {row['sum']}")
    await m.answer("\n".join(lines), parse_mode="Markdown")

# Calendar skeleton
@router.message(Command('link_calendar'))
async def link_cal(m: Message):
    await m.answer("Calendar OAuth hali yoqilmagan (skeleton). Google Cloud sozlangandan keyin havola chiqadi.")

@router.message(Command('calendar_on'))
async def cal_on(m: Message):
    await m.answer("Calendar watch: TODO (Google API).")

@router.message(Command('calendar_test'))
async def cal_test(m: Message):
    await m.answer("Calendar test: yaqin eventlar — TODO.")
