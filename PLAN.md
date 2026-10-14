# Project Plan — Mini Fitness Coach

แผนการพัฒนาโปรเจกต์ Mini Fitness Coach แบ่งเป็น 4 Sprint: Sprint 1, Sprint 2, Sprint 3 และ Final Sprint

> หัวข้อที่ขึ้นต้นด้วย `TODO` เป็นข้อมูลที่ทีมต้องกรอกหรือยืนยันเอง

## 1. ภาพรวมโปรเจกต์

| หัวข้อ | รายละเอียด |
|--------|-----------|
| ชื่อโปรเจกต์ | Mini Fitness Coach |
| Domain | Health / Fitness Application |
| ภาษาและเครื่องมือ | Python, PySide6, SQLite, matplotlib, requests, pytest |
| API | ExerciseDB API (V1 Free API) — https://exercisedb.dev/ |
| Programming Style | Functional Programming Style + Modular Architecture |
| Repository | https://github.com/nattakitkul/mini-fitness-coach |

**เป้าหมาย:** สร้างโปรแกรมที่แนะนำท่าออกกำลังกายตามกลุ่มกล้ามเนื้อจาก ExerciseDB API บันทึก Workout ลง SQLite และวิเคราะห์ Performance รายสัปดาห์พร้อมกราฟ โดยมีโครงสร้างแบบ Modular, Unit Tests และ CI/CD

## 2. บทบาทในทีม

| ชื่อ | บทบาท | หน้าที่ |
|------|-------|---------|
| นายนันทกร โนนกลาง | Project Manager / CI-CD Integrator | วางแผน Sprint และลำดับการพัฒนา, ออกแบบ Program Flow/Menu, วางโครงสร้าง SQLite, จัดทำเอกสาร, ติดตามความคืบหน้า, จัดการ GitHub และ CI/CD |
| นายณัฐกิตติ์ กุลวงศ์ | Automated Tester & QA | เขียนและรัน Unit Tests ด้วย `pytest`, ทดสอบ API/Exception Handling/SQLite, ตรวจ Edge Cases และ Invalid Inputs, ค้นหาและแก้ Bugs |
| นายวรากร โสภา | Core Developer | พัฒนาและเชื่อมต่อ ExerciseDB API, Exercise Suggestion, Workout Logger, Weekly Performance + Chart และเชื่อมต่อส่วนต่างๆ ของระบบ |

## 3. ภาพรวม Sprint

| Sprint | หัวข้อหลัก | ผลลัพธ์ | สถานะ |
|--------|-----------|---------|-------|
| Sprint 1 | CLI Interface & Input Validation | CLI Prototype, pytest 9 tests ผ่าน | เสร็จแล้ว |
| Sprint 2 | Core Workout Features | API + SQLite + Logger + Weekly Chart, pytest 13 tests ผ่าน | เสร็จแล้ว |
| Sprint 3 | GUI Application & User Experience | Desktop GUI ด้วย PySide6 | เสร็จแล้ว (มี Technical Issues ที่แก้ใน Final Sprint) |
| Final Sprint | Stability, Testing, DevOps & Documentation | ระบบเสถียร, เทสและ CI ครบ, เอกสารสมบูรณ์ | กำลังดำเนินการ |

---

## 4. Sprint 1 — CLI Interface & Input Validation

**เป้าหมาย:** สร้างโครงสร้างพื้นฐานของโปรแกรมผ่าน CLI ให้ผู้ใช้เลือกเมนู กรอกข้อมูล และมีการตรวจสอบ Input พร้อมทดสอบด้วย pytest

### งานที่ทำ
- [x] สร้างโครงสร้างโปรเจกต์ Python และใช้ Git/GitHub
- [x] สร้าง Main Menu, Exercise Suggestion Menu, Workout Logger Menu, Weekly Performance Menu
- [x] เพิ่มการตรวจสอบ `is_valid_menu_choice()`, `is_valid_exercise_choice()`, `is_valid_date()` (รูปแบบ `YYYY-MM-DD`)
- [x] จัดการกรณีผู้ใช้กรอกข้อมูลไม่ถูกต้อง
- [x] เขียน Unit Tests 9 รายการ (ผลรัน: 9 passed)

### Definition of Done
- โปรแกรมรันได้ ทุกเมนูเข้าและกลับได้ ใส่ค่าผิดแล้วไม่ crash
- pytest ผ่านทั้งหมด 9 tests และ Source Code อยู่บน GitHub

### ผลลัพธ์
CLI Prototype ที่เลือกเมนู เลือก Muscle Group และกรอกข้อมูล Workout ได้ (ยังไม่เชื่อม API/ฐานข้อมูล)

---

## 5. Sprint 2 — Core Workout Features

**เป้าหมาย:** พัฒนาจาก CLI Prototype ให้เป็นโปรแกรมบันทึกและติดตามการออกกำลังกายได้จริง

### งานที่ทำ
- [x] เชื่อม ExerciseDB API (`api.py`) พร้อม Map กลุ่มกล้ามเนื้อไปยัง body part และจัดการ Request ไม่สำเร็จ/Timeout
- [x] สร้าง SQLite Database (`data/fitness.db`) และตาราง `workouts`
- [x] Workout Logger บันทึกลงฐานข้อมูล (`log_workout()`)
- [x] Workout History (`get_workout_history()`)
- [x] Weekly Performance: Workout Count, Exercise Frequency, Total Sets ในช่วง 7 วันล่าสุด (`get_weekly_performance()`)
- [x] Weekly Chart ด้วย matplotlib (`get_weekly_sets()`, `show_weekly_chart()`)
- [x] เพิ่ม `data/` ใน `.gitignore` ไม่ให้ commit ฐานข้อมูลจริง
- [x] Unit Tests รวม 13 รายการ (ผลรัน: 13 passed)

### Definition of Done
- Exercise Suggestion ดึงข้อมูลจาก API ได้ / บันทึกและดูประวัติจาก SQLite ได้
- Weekly Performance และกราฟแสดงผลได้ / pytest ผ่าน 13 tests / Source Code อยู่บน GitHub

### ผลลัพธ์
โปรแกรม CLI ที่ใช้ฟังก์ชันหลักได้ครบ (Commit สำคัญ: `3a00d94`, `39874e5`)

---

## 6. Sprint 3 — GUI Application & User Experience

**เป้าหมาย:** พัฒนาเป็น Desktop Application ด้วย PySide6 โดยนำฟีเจอร์จาก Sprint 2 มาเชื่อมกับ GUI

### งานที่ทำ
- [x] Main Window พร้อม Sidebar Navigation (`QStackedWidget`) และหน้า Home, Workouts, Exercises, Progress, Records, Goals
- [x] Exercise Library: เลือก Muscle Group, แสดง Exercise Card, หน้า Exercise Detail (Target/Secondary Muscles, Equipment, Instructions, GIF)
- [x] โหลด GIF ผ่าน Background Thread (`QThread`) และแสดงด้วย `QMovie`
- [x] Workout Programs (Beginner Full Body, Chest & Triceps, Leg Day) และ Workout Session
- [x] Records และ Progress เชื่อมกับ SQLite
- [x] แยกโมดูล `analysis.py` และ `charts.py`
- [x] ทดสอบ GUI แบบ Manual และ pytest ชุดเดิม 13 tests ผ่าน

### Technical Issues ที่ส่งต่อไป Final Sprint
- Matplotlib QtAgg ใช้ร่วมกับ PySide6 ไม่ได้ (Import error) จึงฝังกราฟใน GUI ไม่สำเร็จ
- QThread Lifecycle มี warning "Destroyed while thread is still running"
- Navigation และ Workout Flow บางส่วนยังปรับปรุง UX ได้

### ผลลัพธ์
GUI ใช้งาน Exercise Library, Workouts, Records และ Progress ได้ (Commit สำคัญ: `4acfd1e`)

---

## 7. Final Sprint — Stability, Testing, DevOps & Documentation

**เป้าหมาย:** ทำให้ระบบเสถียร ทดสอบครบ ตั้ง CI/CD และจัดทำเอกสารให้พร้อมส่ง

### งานที่ทำเสร็จแล้ว
- [x] ปรับฐานข้อมูลเป็น `sessions` + `sets` (1 แถว = 1 เซ็ตจริง) พร้อม migration จากตาราง `workouts`
- [x] Workout Session แก้ไขเซ็ตได้ (เพิ่ม/ลบเซ็ต ปรับ reps/weight)
- [x] ฝังกราฟ matplotlib ในหน้า Progress สำเร็จ (ล็อกลำดับ import `matplotlib.dates` ก่อน PySide6) และเติม 0 ให้วันที่ไม่มี Workout เพื่อแสดงครบ 7 วัน
- [x] แก้ QThread Lifecycle ด้วยคลาส `Worker` + `cleanup()` และป้องกันผลจาก API ที่มาช้า (request counter / token)
- [x] ปรับปรุง API: ดึงทีละ body part แล้วสลับผล (Legs/Arms), จัดการ HTTP 429, `find_exercise_by_name()` สำหรับ Workout Program
- [x] Personal Records (Stretch) และ CSV Export (Stretch)
- [x] Refactor: `charts.py` ใช้ร่วมกันทั้ง GUI และ CLI, pure functions ใน `analysis.py`
- [x] จัดทำ `README.md`, `plan.md`

### Definition of Done
- `pytest` ผ่านทั้งหมด (รวมเทสใหม่) และ CI ขึ้นเขียวบน GitHub
- README, plan และรายงาน Sprint ตรงกับโปรเจกต์จริง
- โปรแกรมรันได้บนเครื่องที่ติดตั้งจาก `requirements.txt`

รายงานผลของ Sprint นี้อยู่ที่ [`final sprint.md`](final%20sprint.md)

---

## 8. สถานะ Stretch Features (จาก Project Pitch)

| Feature | สถานะ |
|---------|-------|
| CSV Export | ทำแล้ว |
| Personal Best | ทำแล้ว (หน้า Records) |
| Favorite Exercise | ยังไม่ได้ทำ |
| Monthly Statistics | ยังไม่ได้ทำ |
| AI-Assisted Recommendation | ยังไม่ได้ทำ — **TODO ตัดสินใจว่าจะทำหรือไม่ และระบุเหตุผล** |

## 9. Evaluation Checklist (ติดตามจาก Project Pitch)

| Requirement | สถานะ |
|-------------|-------|
| Python Application | ทำแล้ว |
| Public API Integration / `requests` / JSON Parsing | ทำแล้ว (ExerciseDB) |
| SQLite Persistence | ทำแล้ว |
| Functional Style / Modular Functions / Separation of Concerns | ทำแล้ว |
| Exception Handling | ทำแล้ว (API timeout, 429, JSON error, OSError ตอน export) |
| Data Visualization | ทำแล้ว (matplotlib, ฝังใน GUI) |
| Unit Testing (`pytest`) | มีแล้ว แต่ต้องอัปเดตให้ตรง schema ใหม่ |
| Database Testing | ต้องเขียนใหม่ (TODO) |
| API Mock Testing | ยังไม่มี (TODO) |
| GitHub | ใช้งานแล้ว |
| CI/CD (GitHub Actions) | TODO |
| Code Quality (PEP8 / linting) | TODO |
| CSV Export | ทำแล้ว (Stretch) |
| AI Feature | ยังไม่ได้ทำ (Stretch) |

## 10. ความเสี่ยงและแนวทางรับมือs

| ความเสี่ยง | แนวทางรับมือ |
|-----------|--------------|
| ExerciseDB API ช้า ล่ม หรือจำกัดจำนวนคำขอ | Timeout, ข้อความแจ้งผู้ใช้, โหลดใน Background Thread, แคช GIF |
| เทสเขียนลงฐานข้อมูลจริงหรือล้าสมัยหลังเปลี่ยน schema | ใช้ฐานข้อมูลชั่วคราวในทุกเทส และให้ CI รันเทสทุกครั้งที่ push |
| ข้อมูลจากโครงสร้างฐานข้อมูลเดิม | Migration อัตโนมัติ เปลี่ยนชื่อตารางเก่าเป็น `workouts_legacy` ไม่ลบข้อมูล |
| Import order ของ matplotlib/PySide6 | ล็อก `import matplotlib.dates` เป็นบรรทัดแรกของ `app.py` |
| เครือข่ายตรวจ SSL ไม่ผ่าน | ใช้สวิตช์ `VERIFY_SSL` ใน `api.py` |