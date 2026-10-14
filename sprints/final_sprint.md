# แบบรายงานผลการดำเนินงาน Final Sprint

- **ชื่อโปรเจกต์:** Mini Fitness Coach
- **สัปดาห์ที่:** 4 (Final Sprint: Stability, Testing, DevOps & Documentation)
- **สมาชิกในทีม:**
  - Project Manager / CI-CD Integrator: นายนันทกร โนนกลาง
  - Automated Tester & QA: นายณัฐกิตติ์ กุลวงศ์
  - Core Developer: นายวรากร โสภา
- **GitHub Repository:** https://github.com/nattakitkul/mini-fitness-coach

> **หมายเหตุ:** หัวข้อที่ขึ้นต้นด้วย `TODO` เป็นข้อมูลที่ต้องให้ทีมกรอกหรือยืนยันเอง (เช่น ผลการรันจริง สถานะ CI คะแนนประเมิน) ควรลบคำว่า TODO ออกหลังกรอกแล้ว

---

## 1. สรุปความก้าวหน้าของงาน (Sprint Progress Summary)

### 1.1 งานที่ทำเสร็จแล้วใน Final Sprint

- [x] **ปรับโครงสร้างฐานข้อมูลใหม่** จากตาราง `workouts` (1 แถว = 1 ท่า) เป็น `sessions` + `sets` (1 แถว = 1 เซ็ตจริง) เพื่อให้บันทึกแต่ละเซ็ตที่มี reps/weight ต่างกันได้ และนับจำนวน "ครั้งที่ออกกำลังกาย" ได้ถูกต้อง
- [x] **Migration ข้อมูลเก่า** ฟังก์ชัน `_migrate_old_workouts()` ย้ายข้อมูลจากตารางเดิมเข้าตารางใหม่อัตโนมัติ และเปลี่ยนชื่อตารางเก่าเป็น `workouts_legacy` (ไม่ลบข้อมูล)
- [x] **CSV Export** (`export_history_csv()` ใน `analysis.py`) ส่งออกประวัติทั้งหมด 1 แถวต่อ 1 เซ็ต เรียงจากเก่าไปใหม่ ใช้ `utf-8-sig` เพื่อให้ Excel แสดงข้อความที่ไม่ใช่ภาษาอังกฤษได้ถูกต้อง และมีปุ่ม Export ในหน้า Records
- [x] **Personal Records** (`get_personal_records()`) แสดงน้ำหนักสูงสุดและจำนวน reps สูงสุดของแต่ละท่าในหน้า Records
- [x] **Weekly Chart แบบ Embedded** ฝังกราฟ matplotlib ในหน้า Progress ของ GUI สำเร็จ (แก้ปัญหา QtAgg ที่ค้างจาก Sprint 3 ดูหัวข้อ 5)
- [x] **กราฟแสดงครบ 7 วันเสมอ** ฟังก์ชัน `fill_missing_days()` เติม 0 ให้วันที่ไม่มี Workout และแสดงข้อความ "No workouts in the last 7 days" เมื่อไม่มีข้อมูล
- [x] **แก้ไข QThread Lifecycle** เพิ่มคลาส `Worker` ที่เก็บ reference ไว้ใน `_threads` จนกว่า thread จะจบ และมีฟังก์ชัน `cleanup()` รอ thread ก่อนปิดโปรแกรม
- [x] **ป้องกันผลลัพธ์จาก API ที่มาช้า** ใช้ request counter (หน้า Exercises) และ token (หน้า Exercise Detail) เพื่อไม่ให้ผลของคำขอเก่ามาทับหน้าปัจจุบัน
- [x] **Workout Session แก้ไขเซ็ตได้** เพิ่ม/ลบเซ็ต ปรับ reps และ weight ได้ระหว่างออกกำลังกาย เซ็ตใหม่เริ่มด้วยค่าจากเซ็ตก่อนหน้า
- [x] **Exercise Detail ดึงรายละเอียดเพิ่ม** Workout Program เก็บแค่ชื่อท่า จึงมี `find_exercise_by_name()` ไปค้นหา GIF, Target Muscle และ Instructions เพิ่มจาก API
- [x] **ปรับปรุงการดึงข้อมูลจาก API** กลุ่ม Legs/Arms ดึงทีละ body part แล้วสลับผลลัพธ์ (interleave) เพื่อให้ได้ทั้ง upper/lower และไม่ซ้ำ จัดการ HTTP 429 (rate limit) และ Timeout ด้วยข้อความที่เหมาะสม
- [x] **ปรับ UI** ธีม Dark minimal, ปุ่ม Show more ในหน้า Exercises, Sidebar แบบ checkable
- [x] **Refactor** แยก `charts.py` ให้ใช้ร่วมกันทั้ง GUI และ CLI และแยก pure functions ใน `analysis.py` ออกจากส่วนที่เรียกฐานข้อมูล
- [x] **เอกสาร** จัดทำ `README.md` และ `plan.md`

### 1.2 งานที่ยังต้องทำ / ยืนยันก่อนส่ง

- [ ] **TODO – แก้ Unit Tests ที่ล้าสมัย** `tests/test_database.py` ยังเรียก `log_workout()` / `get_workout_history()` และตาราง `workouts` ซึ่งถูกแทนที่แล้ว ต้องเขียนใหม่ให้ใช้ `save_session()`, `get_history()`, `get_personal_records()`, `get_weekly_performance()`
- [ ] **TODO – แยก Test ออกจากฐานข้อมูลจริง** เทสบางตัวใน `test_main.py` (เช่น `test_workout_menu`) เขียนลง `data/fitness.db` จริง ต้อง mock path ด้วย `tmp_path` และ `monkeypatch`
- [ ] **TODO – เพิ่ม Test ใหม่** สำหรับ `analysis.py` (`last_7_days`, `fill_missing_days`, `history_to_rows`, `export_history_csv`) และ API Mock Test สำหรับ `api.py` (ไม่เรียก network จริง) ตาม Evaluation Checklist ใน Project Pitch
- [ ] **TODO – CI/CD (GitHub Actions)** ตั้งค่า workflow ให้รัน `flake8` + `pytest` อัตโนมัติเมื่อ push / เปิด Pull Request เข้า `main` และยืนยันว่าสถานะขึ้นเขียวบน GitHub
- [ ] **TODO – `requirements.txt`** ระบุ `PySide6`, `matplotlib`, `requests`, `pytest`, `flake8`
- [ ] **TODO – หน้า Home และ Goals** ยังเป็นหน้าเปล่า ต้องทำให้เสร็จหรือตัดออกจาก Sidebar
- [ ] **TODO – AI Feature** (Stretch ใน Project Pitch) ตัดสินใจว่าจะทำหรือไม่ ถ้าไม่ทำให้ระบุเหตุผลในหัวข้อ 3

---

## 2. ผลการทดสอบระบบ (Quality Assurance & Debugging Report)

### 2.1 Unit Tests (`pytest`)

| รายการ | สถานะ |
|---|---|
| ผลรัน `pytest -v` ล่าสุด | **TODO – กรอกจำนวน passed / failed หลังแก้เทสเสร็จ** |
| ไฟล์ที่ต้องแก้ | `tests/test_database.py` (เรียกฟังก์ชันและตารางที่ไม่มีแล้ว) |
| ไฟล์ที่ต้องแยกจากฐานข้อมูลจริง | `tests/test_main.py` |

ประวัติจำนวนเทสที่ผ่านมา: Sprint 1 = 9 tests, Sprint 2 = 13 tests, Sprint 3 = 13 tests (ชุดเดิม)

### 2.2 Lint (`flake8`)

**TODO – กรอกผลรัน `flake8 src/ tests/` (จำนวน error และวิธีแก้)**

### 2.3 Manual / Integration Testing (Expected / Actual)

ตารางนี้ระบุผลที่คาดหวังจากการทำงานของโค้ดปัจจุบัน ส่วน **ผลจริง** และ **สถานะ** ให้ผู้ทดสอบกรอกหลังลองใช้งานจริง

| รายการทดสอบ | ขั้นตอน / อินพุต | ผลลัพธ์ที่คาดหวัง (Expected) | ผลการทดสอบจริง (Actual) | สถานะ |
|---|---|---|---|---|
| บันทึก Workout จาก Session | เริ่ม Beginner Full Body → ปรับเซ็ต → Finish Workout | มี popup สรุปจำนวนท่าและเซ็ต, เปิดหน้า Progress, ข้อมูลอยู่ใน Records | TODO | TODO |
| บันทึก Session ที่ไม่มีเซ็ต | `save_session()` ด้วย exercises ว่าง | คืนค่า `None` และแสดงเตือน "This workout has no sets." | TODO | TODO |
| ลบเซ็ตจนเหลือ 1 | กด "− Remove set" ซ้ำ ๆ | เหลืออย่างน้อย 1 เซ็ต ไม่ลบจนหมด | TODO | TODO |
| Weekly Performance | บันทึก 2 sessions ในสัปดาห์เดียวกัน | Workouts = 2, Total sets ตรงกับจำนวนเซ็ตจริง | TODO | TODO |
| กราฟไม่มีข้อมูล | ฐานข้อมูลว่าง / ไม่มี Workout 7 วันล่าสุด | แสดงกราฟว่างพร้อมข้อความ "No workouts in the last 7 days" | TODO | TODO |
| กราฟวันที่ไม่มี Workout | มี Workout เพียงบางวัน | แกน X แสดงครบ 7 วัน วันที่ไม่มีข้อมูลเป็น 0 | TODO | TODO |
| Personal Records | บันทึกท่าเดียวกัน 2 ครั้งด้วยน้ำหนักต่างกัน | แสดงน้ำหนักสูงสุดและ reps สูงสุดของท่านั้น | TODO | TODO |
| CSV Export | หน้า Records → Export CSV → เลือกที่บันทึก | ได้ไฟล์ `.csv` 1 แถวต่อเซ็ต เปิดใน Excel ได้ | TODO | TODO |
| CSV Export ไม่มีข้อมูล | กด Export ตอนยังไม่มี Workout | แสดงเตือน "There are no workout records yet." | TODO | TODO |
| CSV Export ไฟล์ถูกเปิดค้างอยู่ | บันทึกทับไฟล์ที่เปิดใน Excel | แสดงข้อความ "Export failed" ไม่ crash | TODO | TODO |
| Exercise Library | เลือก Chest / Legs / Arms | แสดง Exercise Card พร้อม GIF, Legs/Arms ผสมทั้ง 2 body part | TODO | TODO |
| คลิกเปลี่ยน Muscle Group เร็ว ๆ | คลิก Chest แล้วรีบคลิก Back | แสดงเฉพาะผลของ Back (ไม่มีผล Chest มาทับ) | TODO | TODO |
| Exercise Detail จาก Program | Workouts → Start → กด "Details" | โหลดรายละเอียด/GIF เพิ่มจาก API ปุ่ม Start ถูกซ่อน | TODO | TODO |
| API ใช้งานไม่ได้ | ปิดอินเทอร์เน็ตแล้วเปิดหน้า Exercises | แสดง "No exercises found." และไม่ crash | TODO | TODO |
| ย้ายข้อมูลเก่า | เปิดโปรแกรมกับ `fitness.db` ที่มีตาราง `workouts` | ข้อมูลถูกย้ายเข้า `sessions`/`sets`, ตารางเก่าเปลี่ยนเป็น `workouts_legacy` | TODO | TODO |
| ปิดโปรแกรมระหว่างโหลด GIF | เปิดหน้า Exercises แล้วปิดหน้าต่างทันที | ไม่มี error "QThread: Destroyed while thread is still running" | TODO | TODO |
| CLI | `python -m src.main` ทดสอบทุกเมนู | ทุกเมนูทำงานได้ ใส่ค่าผิดแล้วไม่ crash | TODO | TODO |

---

## 3. สรุปบทเรียนประจำสัปดาห์ (Retrospective: Wow! & Whoops!)

- **Wow!** (ส่วนที่ทำได้ดี):
  - การออกแบบฐานข้อมูลใหม่เป็น `sessions` + `sets` ทำให้ข้อมูลตรงกับการออกกำลังกายจริงมากขึ้น และเปิดทางให้ทำ Personal Records และ CSV Export ได้ง่าย
  - การแยกโค้ดเป็นโมดูล (`api.py`, `database.py`, `analysis.py`, `charts.py`) และแยก pure functions ออกจากส่วนที่ต่อฐานข้อมูล ทำให้ GUI และ CLI ใช้ตรรกะเดียวกันและทดสอบง่าย
  - โปรเจกต์พัฒนาตามแผนจาก CLI Prototype (Sprint 1) → Core Features (Sprint 2) → GUI (Sprint 3) → เสถียรภาพ (Final Sprint) และทำ Stretch Features ได้หลายข้อ (Favorite ยังไม่ได้ทำ แต่ CSV Export และ Personal Best ทำแล้ว)

- **Whoops!** (ปัญหาที่พบและแนวทางแก้ไข):
  - หลังเปลี่ยนโครงสร้างฐานข้อมูล **Unit Tests ที่เขียนไว้ก่อนหน้าไม่ได้ถูกอัปเดตตาม** ทำให้เทสบางไฟล์ล้าสมัยและบางตัวเขียนลงฐานข้อมูลจริง บทเรียนคือควรแก้เทสพร้อมกับการเปลี่ยน schema ทุกครั้ง และให้ CI รันเทสอัตโนมัติเพื่อจับปัญหานี้ได้เร็ว
  - การ import `matplotlib` หลัง `PySide6` ทำให้เกิด error จึงต้องล็อกลำดับ import ไว้ (ดูหัวข้อ 5)
  - **TODO – ทีมเพิ่มบทเรียนอื่นที่เจอจริงเพิ่มเติม**

- **เหตุผลที่ยังไม่ทำ / ตัดออก:** **TODO – ระบุ เช่น Favorite Exercise, Monthly Statistics, AI-Assisted Recommendation (Stretch ใน Project Pitch)**

---

## 4. สิ่งที่ต้องทำต่อก่อนส่งงาน Final Sprint

- [ ] **TODO – แก้และรัน `pytest` ให้ผ่านทั้งหมด** (ดูหัวข้อ 1.2)
- [ ] **TODO – ตั้งค่า GitHub Actions และยืนยันสถานะเขียวบน GitHub**
- [ ] **TODO – ทดสอบ Manual ตามตารางหัวข้อ 2.3 และกรอกผลจริง**
- [ ] **TODO – ทดสอบรันบนเครื่องที่สะอาด** (สร้าง virtual environment ใหม่ → `pip install -r requirements.txt` → `python -m src.app`)
- [ ] **TODO – ซ้อมนำเสนอ / Live Demo** ตามลำดับ: Exercises → Workouts → Session → Progress → Records → Export CSV
- [ ] **TODO – กรอกตาราง Self-Assessment** (หัวข้อ 6)
- [ ] **TODO – กำหนดวันส่ง:** ____/____/____

---

## 5. ปัญหาทางเทคนิคที่เจอและวิธีแก้ไข (Technical Issues & Fixes)

| ปัญหาที่เจอ | อาการที่พบ | สาเหตุ | วิธีแก้ไข |
|---|---|---|---|
| Matplotlib QtAgg ใช้ร่วมกับ PySide6 ไม่ได้ (ค้างจาก Sprint 3) | เกิด `AttributeError` ตอน import Qt backend ของ Matplotlib | `matplotlib.dates` โหลด `dateutil`/`six` ซึ่งพังถ้า `PySide6` ถูก import ไปก่อน | import `matplotlib.dates` เป็นบรรทัดแรกของ `app.py` พร้อมคอมเมนต์กำกับ ทำให้ฝังกราฟด้วย `FigureCanvasQTAgg` ได้ |
| `QThread: Destroyed while thread is still running` (ค้างจาก Sprint 3) | มี warning ตอนปิดโปรแกรม/ปิดหน้าขณะโหลด | Thread ถูกทำลายก่อนทำงานเสร็จ เพราะไม่มีใครถือ reference | ให้ `Worker` เก็บตัวเองไว้ในเซ็ต `_threads` จนจบงาน และเรียก `cleanup()` ตอน `aboutToQuit` เพื่อรอ thread แล้วลบไฟล์ GIF ชั่วคราว (**TODO – ยืนยันว่า warning หายไปจากการทดสอบจริง**) |
| ผลจาก API ที่มาช้ามาทับหน้าที่ผู้ใช้เปลี่ยนไปแล้ว | กดเปลี่ยน Muscle Group เร็ว ๆ แล้วเห็นรายการของกลุ่มเก่า | คำขอเก่าเสร็จทีหลังคำขอใหม่ | ใช้หมายเลขคำขอ (`exercise_request`) และ `token` ใน Detail Page เพื่อทิ้งผลลัพธ์ที่ล้าสมัย |
| GUI ค้างขณะโหลดข้อมูลจาก Network | หน้าต่างไม่ตอบสนองตอนโหลด Exercise/GIF | เรียก `requests` ใน Main Thread | ย้ายงาน Network ไปทำใน `Worker` (QThread) แล้วส่งผลกลับ Main Thread ด้วย Signal |
| Legs/Arms แสดงท่าไม่ครบทุกส่วน | แสดงแต่ท่าของ body part ที่ API ส่งมาก่อน | API คืนผลของหลาย body part รวมกัน | ขอทีละ body part แล้วสลับผลลัพธ์ พร้อมตัดท่าที่ซ้ำ |
| จำนวน "Workouts" ในสัปดาห์นับผิด | นับเป็นจำนวนท่า ไม่ใช่จำนวนครั้งที่ไปออกกำลังกาย | ตาราง `workouts` เก็บ 1 แถวต่อ 1 ท่า ไม่มีแนวคิด session | ออกแบบ `sessions` + `sets` ใหม่ และนับ `COUNT(DISTINCT s.id)` |
| กราฟรายสัปดาห์แสดงเฉพาะวันที่มีข้อมูล | แกน X ไม่ครบ 7 วัน | SQL คืนเฉพาะวันที่มี Workout | `fill_missing_days()` เติม 0 ให้วันที่ว่าง |
| ไฟล์ CSV เปิดใน Excel แล้วข้อความเพี้ยน | อักขระที่ไม่ใช่ภาษาอังกฤษอ่านไม่ออก | Excel ไม่รู้ว่าเป็น UTF-8 | เขียนไฟล์ด้วยการเข้ารหัส `utf-8-sig` (มี BOM) |
| การตรวจสอบ SSL ถูกปิดอยู่ | โค้ดเดิมเรียก API ด้วย `verify=False` | เครือข่ายบางแห่งตรวจใบรับรองไม่ผ่าน | รวมเป็นสวิตช์เดียว `VERIFY_SSL` ใน `api.py` (ตอนนี้ปิดอยู่ **TODO – ลองเปิดเป็น `True` ถ้าเครือข่ายรองรับ**) |
| Unit Tests ล้าสมัยหลังเปลี่ยน schema | `test_database.py` เรียก `log_workout`, `get_workout_history` และตาราง `workouts` ที่ไม่มีแล้ว | เปลี่ยนโครงสร้างฐานข้อมูลโดยไม่ได้แก้เทสตาม | **ยังไม่ได้แก้ — อยู่ในรายการงานหัวข้อ 1.2** |

---

## 6. ผลการประเมินตนเอง (Self-Assessment)

**Group Self-Assessment (0–10)**

| หัวข้อ | น้ำหนัก | คะแนนกลุ่ม (0-10) | เหตุผล |
|---|---|---|---|
| บรรลุวัตถุประสงค์กลุ่ม | 30% | TODO | TODO |
| ความสอดคล้องของเนื้อหาและมาตรฐานของงาน | 30% | TODO | TODO |
| ปริมาณ คุณภาพ และธรรมาภิบาลของงาน | 30% | TODO | TODO |
| ภาพรวมงานกลุ่มทั้งหมด | 10% | TODO | TODO |
| **รวม (ถ่วงน้ำหนัก)** | **100%** | **TODO / 10** | |

**Individual Self-Assessment (0–10)**

| ชื่อ | หน้าที่ | ความรับผิดชอบ | การมีส่วนร่วมและทำงานเป็นทีม | การสื่อสารและทัศนคติ | รวม |
|---|---|---|---|---|---|
| นายนันทกร โนนกลาง | Project Manager / CI-CD Integrator | TODO | TODO | TODO | TODO |
| นายณัฐกิตติ์ กุลวงศ์ | Automated Tester & QA | TODO | TODO | TODO | TODO |
| นายวรากร โสภา | Core Developer | TODO | TODO | TODO | TODO |