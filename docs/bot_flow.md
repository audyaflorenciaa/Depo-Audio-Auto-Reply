# DA AUTOLIGHT AI — Conversation Flow & State Machine

> This document defines the **complete conversation tree**, all valid state transitions,
> guardrail rules, and the human handoff trigger conditions.

---

## 1. State Machine Overview

The bot operates as a **strict finite-state machine (FSM)**. It does not hold a free-form conversation.
Every message from the user either advances the state forward, triggers clarification, or triggers handoff.

### State Definitions

| State ID | Name | Description |
|---|---|---|
| `S0` | `IDLE` | No conversation active yet |
| `S1` | `GREETED` | Bot sent the greeting; waiting for customer's first intent |
| `S2` | `GATHERING_CAR_INFO` | Asking for car brand and year |
| `S3` | `CAR_INFO_CONFIRMED` | Car brand and year captured |
| `S4` | `GOAL_ASSESSMENT` | Asking Function vs. Aesthetics preference |
| `S5` | `RECOMMENDATION_FUNCTION` | Customer wants function; showing Foglamp prices |
| `S6` | `RECOMMENDATION_AESTHETICS` | Customer wants aesthetics; showing Headlamp prices |
| `S7` | `RECOMMENDATION_BOTH` | Customer wants both; showing combo recommendation |
| `S8` | `FOLLOWUP` | Customer has follow-up question within scope |
| `S9` | `HANDOFF` | Conversation handed off to human staff |
| `S10` | `CLOSED` | Conversation completed |

---

## 2. State Transition Diagram

```
[S0: IDLE]
    |
    | User sends ANY message (first contact)
    v
[S1: GREETED]
    |  Bot sends official greeting (verbatim, no changes)
    |  Bot asks: "Ada yang bisa dibantu?"
    |
    | User responds (any intent)
    v
[S2: GATHERING_CAR_INFO]
    |  Bot asks: "Boleh tahu mobil apa dan tahun berapa?"
    |
    | User provides car brand + year
    v
[S3: CAR_INFO_CONFIRMED]
    |  Bot confirms: "Oke, untuk [Brand] tahun [Year]..."
    |
    | Immediately transitions to →
    v
[S4: GOAL_ASSESSMENT]
    |  Bot asks: Function vs. Aesthetics question
    |
    |--[User says FUNCTION]---------> [S5: RECOMMENDATION_FUNCTION]
    |                                      |
    |--[User says AESTHETICS]-------> [S6: RECOMMENDATION_AESTHETICS]
    |                                      |
    |--[User says BOTH]-------------> [S7: RECOMMENDATION_BOTH]
    |                                      |
    |--[User is unclear/off-script]-> [S9: HANDOFF]
    
[S5 / S6 / S7] --> [S8: FOLLOWUP] if user asks in-scope follow-up
[S5 / S6 / S7 / S8] --> [S9: HANDOFF] if user asks out-of-scope, wants to book, or is unpredictable
[S5 / S6 / S7 / S8] --> [S10: CLOSED] if user says thank you / goodbye
```

---

## 3. Exact Bot Messages Per State

### S1 — Official Greeting (VERBATIM — DO NOT MODIFY)

```
👋 Halo! Terima kasih sudah menghubungi DA AUTOLIGHT (Depo Audio).

📩 Jam operasional: 09.00 – 17.00 WIB
❌ Libur setiap hari SELASA (2 minggu sekali).

❓️ Untuk konsultasi offline bisa langsung datang ke workshop kami di Jakarta Timur.
💡 Bisa test cahaya langsung sampai benar-benar yakin sebelum pemasangan!

INSTAGRAM: https://www.instagram.com/variasi_depoaudio
TIKTOK: https://www.tiktok.com/@depoaudio_variasi
LOKASI: https://share.google/J1MXaIoQOvzN5qjmT

Ada yang bisa dibantu?
```

> **Rule:** This message must be sent character-for-character on first contact.
> The bot must not paraphrase, shorten, or translate it.

---

### S2 — Car Info Gathering

**Bot message:**
```
Boleh tahu mobil apa dan tahun berapa, Kak? 😊
Contoh: Toyota Avanza 2020, Honda Jazz 2018, dll.
```

**Entities to extract:**
- `car_brand` (string) — e.g., "Toyota", "Honda", "Mitsubishi"
- `car_year` (integer) — e.g., 2019
- `car_model` (string, optional) — e.g., "Avanza", "Pajero"

**Validation:**
- Year must be a plausible car year (1990–2026). Reject anything outside this range.
- If the user gives only the brand without the year (or vice versa), ask again specifically for what is missing.

---

### S3 — Car Info Confirmed

**Bot message (template — fill in extracted values):**
```
Oke, untuk [car_brand] [car_model] tahun [car_year] ya 👍

Sekarang, boleh tahu tujuannya apa?
```
Then immediately ask the goal question (transition to S4).

---

### S4 — Goal Assessment

**Bot message:**
```
Tujuan upgrade lampunya untuk apa nih, Kak?

1️⃣ FUNGSI — Ingin penerangan jalan yang lebih terang dan aman
2️⃣ ESTETIKA — Ingin tampilan lebih keren (demon eyes, DRL, variasi warna)
3️⃣ KEDUANYA — Ingin terang sekaligus keren

Ketik 1, 2, atau 3 ya 😊
```

**Intent mapping:**
- Keywords for FUNCTION: "terang", "jelas", "safety", "fungsi", "hujan", "kabut", "1", "function", "bright"
- Keywords for AESTHETICS: "keren", "gaya", "estetika", "demon", "RGB", "warna", "tampilan", "2", "aesthetics", "look"
- Keywords for BOTH: "keduanya", "dua-duanya", "both", "3"

---

### S5 — Recommendation: FUNCTION (Foglamp)

**Bot message:**
```
Untuk fungsi penerangan, kami rekomendasikan FOGLAMP! 💡

Foglamp dipasang di bawah bumper dan memberikan penerangan jarak dekat yang lebar, 
sehingga tekstur jalan lebih terlihat jelas — sangat bagus untuk berkendara malam atau hujan.

Berikut pilihan Foglamp kami:

--- FOGLAMP 3 INCH ---
PRO7:
• P7.F30 = Rp 2.600.000 (Putih)
• P 735 F SE = Rp 2.800.000 (Putih) ⭐ BEST SELLER
• P 735 FX = Rp 2.950.000 (Putih + Laser)
• P 735 F-3C Apps = Rp 3.250.000 (3 Warna, kontrol via Apps)
• P 755 F = Rp 3.700.000 (Putih sedikit Kuning)

UPS WAYMAKER:
• UPS UF-3 (1 Warna) = Rp 2.350.000 ⭐ BEST SELLER
• UPS UF-3 (3 Warna) = Rp 2.650.000
• UPS Waymaker F75 (Dual Laser) 3 Warna = Rp 3.000.000
• UPS Waymaker F55 3 Warna + Demon RGB = Rp 2.700.000

AES:
• Fx 3 inch 1 Warna = Rp 2.200.000
• Fx 3 inch 3 Warna = Rp 2.300.000
• Fx 3 inch Single Laser = Rp 2.400.000
• Fx 3 inch Double Laser = Rp 2.500.000

DA AUTOLIGHT (In-House):
• 3 inch 1 warna = Rp 1.800.000
• 3 inch 3 warna = Rp 1.900.000

--- FOGLAMP 2 INCH ---
PRO7:
• P 735F-M = Rp 2.600.000
• P 735FX-M (Laser) = Rp 2.900.000
• P735F-M 3C (3 Warna) = Rp 3.150.000

UPS WAYMAKER:
• UF-2 1 Warna = Rp 2.350.000 ⭐ BEST SELLER
• UF-2 3 Warna = Rp 2.500.000

AES:
• FX 2 Inch 1 Warna = Rp 2.200.000
• FX 2 Inch 3 Warna = Rp 2.300.000
• FX 2 Inch Single Laser = Rp 2.400.000
• FX 2 Inch Double Laser = Rp 2.500.000

*Semua harga sudah termasuk pemasangan, leveling, dan relay highbeam.

Ada yang mau ditanyakan soal produk di atas? 😊
Atau kalau mau langsung ke workshop, boleh test cahayanya dulu sebelum beli!
```

---

### S6 — Recommendation: AESTHETICS (Headlamp)

**Bot message:**
```
Untuk tampilan keren, kami rekomendasikan HEADLAMP upgrade! ✨

Headlamp memberikan tampilan OEM yang premium — terlihat seperti bawaan pabrik kelas atas,
dengan opsi Demon Eyes, DRL, dan variasi warna.

Berikut pilihan Headlamp kami:

--- HEADLAMP 3 INCH ---
PRO7:
• P 730 RV = Rp 3.500.000
• P 730 SL = Rp 3.500.000 (Khusus Pajero 2016+ & Fortuner GR)
• P 750 RV = Rp 4.500.000
• P 770 SV = Rp 5.200.000
• P 770 SL = Rp 5.500.000 (Khusus Pajero 2016+ & Fortuner GR)
• P 7RBX = Rp 5.500.000
• P 7MRX = Rp 7.500.000

UPS WAYMAKER:
• S500 V2 = Rp 4.300.000
• S600 = Rp 4.450.000 (Double Laser)
• SL850 = Rp 4.750.000 (Khusus Pajero 2016+ & Fortuner GR)
• G600 = Rp 4.850.000 (Pure Laser)

Harga Terjangkau:
• WST 3 Inch = Rp 2.650.000
• AES Bi-Laser Premium = Rp 3.200.000
• Kuro Raijin R65 = Rp 3.500.000

--- HEADLAMP 2 INCH ---
PRO7:
• P71MX = Rp 2.500.000/set
• P72MX = Rp 3.000.000/set
• P73MX = Rp 3.500.000/set

UPS WAYMAKER:
• SQ 300 = Rp 2.500.000/set
• SQ 600 = Rp 2.750.000/set
• SQ 800 = Rp 3.250.000/set

*Semua harga sudah termasuk pemasangan, poles mika, rakit soket, relay, selongsong kabel, solasi bakar, dan leveling laser.

Untuk inspirasi tampilan, cek IG & TikTok kami ya! 😍
📸 Instagram: https://www.instagram.com/variasi_depoaudio
🎵 TikTok: https://www.tiktok.com/@depoaudio_variasi

Ada pertanyaan lanjutan? 😊
```

---

### S9 — Human Handoff

**Trigger conditions (any of the following):**
1. Customer asks about a service not in the product list (e.g., wiring, sound system, other mods).
2. Customer wants to make a booking or appointment.
3. Customer asks for a discount or negotiation.
4. Customer provides a car that needs special compatibility check.
5. Customer's intent is ambiguous after 2 clarification attempts.
6. Customer sends inappropriate or non-automotive content.
7. Customer explicitly asks to speak to a human/staff.

**Bot message:**
```
Baik, saya akan sambungkan dengan tim kami untuk membantu lebih lanjut 🙏

Mohon tunggu sebentar ya, Kak. Tim kami akan segera merespons.

Atau bisa langsung hubungi kami / datang ke workshop di Jakarta Timur 😊
📍 https://share.google/J1MXaIoQOvzN5qjmT
```

**System action after handoff message:**
1. Set conversation state to `S9: HANDOFF`.
2. Write handoff log entry (timestamp, user ID, last 10 messages, trigger reason).
3. Stop AI auto-reply for this conversation (human takes over).
4. (Future) Ping the staff Telegram group with the customer's details.

---

## 4. Guardrail Rules

These rules are **non-negotiable** and must be enforced at the prompt level:

| Rule # | Rule |
|---|---|
| G1 | The bot MUST NEVER invent or estimate a price not in `product_data.md`. |
| G2 | The bot MUST NEVER promise stock availability (not yet implemented). |
| G3 | The bot MUST NEVER offer discounts or negotiate prices. |
| G4 | The bot MUST NEVER skip states (e.g., go from S1 directly to S5). |
| G5 | The bot MUST send the exact greeting text in S1, verbatim. |
| G6 | The bot MUST ask for car brand and year before giving any recommendation. |
| G7 | If unsure about a customer's intent after 2 tries, the bot MUST trigger handoff. |
| G8 | The bot MUST NOT answer general questions about cars, insurance, registration, etc. |
| G9 | All prices quoted must be copied exactly from `product_data.md`. |
| G10 | If a customer's car model has a special note (e.g., Pajero 2016+), bot must mention it. |

---

## 5. Session & Context Management

- Each Telegram user (`chat_id`) has an independent session.
- Session state is stored in memory (Redis in production, in-memory dict in development).
- Session data structure:

```json
{
  "chat_id": 123456789,
  "state": "S4",
  "car_brand": "Mitsubishi",
  "car_model": "Pajero Sport",
  "car_year": 2019,
  "goal": null,
  "handoff_reason": null,
  "message_history": [],
  "created_at": "2026-09-16T14:00:00+07:00",
  "updated_at": "2026-09-16T14:05:00+07:00"
}
```

- Sessions expire after **24 hours** of inactivity. Returning users start from S1.

---

## 6. Out-of-Scope Topics (Always Trigger Handoff)

- Car audio / sound systems
- Car window tinting
- Car wrapping / vinyl
- Engine or mechanical work
- Car insurance
- Price negotiations / discounts
- Booking appointments (Phase 1 — no booking system yet)
- Anything not related to automotive lighting products listed in `product_data.md`
