# Mini Fitness Coach

โปรแกรมผู้ช่วยออกกำลังกายขนาดเล็กที่เขียนด้วย Python ช่วยให้ผู้ใช้ค้นหาท่าออกกำลังกายตามกลุ่มกล้ามเนื้อ บันทึกการออกกำลังกายทีละเซ็ต และดูสถิติ สถิติส่วนตัวสูงสุด (Personal Records) และกราฟการออกกำลังกายย้อนหลังได้

โปรเจกต์นี้มี 2 หน้าจอที่ใช้ฐานข้อมูลและตรรกะชุดเดียวกัน:

- **Desktop GUI** (PySide6) — `src/app.py`
- **Command-line menu (CLI)** — `src/main.py`

> พัฒนาเป็น 4 Sprint: CLI Prototype → Core Workout Features → GUI Application → Final Sprint (รายละเอียดดูที่ [`plan.md`](plan.md))

## ปัญหาที่โปรเจกต์ต้องการแก้

นักศึกษาและผู้เริ่มต้นออกกำลังกายมักไม่รู้ว่าควรเลือกท่าไหนให้เหมาะกับกล้ามเนื้อที่ต้องการฝึก และไม่มีวิธีที่ง่ายในการจดว่าแต่ละวันทำอะไรไปบ้าง Mini Fitness Coach รวมทั้งสองอย่างไว้ในโปรแกรมเดียว

## ฟีเจอร์

- **Exercise Library** — เลือกกลุ่มกล้ามเนื้อ (Chest, Back, Legs, Shoulders, Arms, Abs) แล้วดูท่าออกกำลังกายพร้อม GIF, Target Muscle, Equipment และ Instructions จาก [ExerciseDB API](https://exercisedb.dev/)
- **Workout Programs** — เริ่มโปรแกรมสำเร็จรูป (Beginner Full Body, Chest & Triceps, Leg Day) หรือเริ่มจากท่าเดียวได้
- **Workout Session / Logger** — บันทึก reps และ weight ของแต่ละเซ็ต เพิ่ม/ลบเซ็ตได้ระหว่างออกกำลังกาย
- **Weekly Progress** — จำนวนครั้งที่ออกกำลังกาย จำนวนท่าที่ต่างกัน และจำนวนเซ็ตรวมใน 7 วันล่าสุด พร้อมกราฟแท่ง (matplotlib) แสดงครบ 7 วัน
- **Personal Records & History** — น้ำหนักสูงสุดและ reps สูงสุดของแต่ละท่า พร้อมประวัติการออกกำลังกายทั้งหมด
- **CSV Export** — ส่งออกประวัติทั้งหมด (1 แถวต่อ 1 เซ็ต) เปิดใน Excel ได้
- **Migration ข้อมูลเก่า** — ย้ายข้อมูลจากตาราง `workouts` แบบเดิมเข้าโครงสร้างใหม่อัตโนมัติ

## Tech Stack

| ส่วน | เทคโนโลยี |
|------|-----------|
| ภาษา | Python 3 |
| GUI | PySide6 (Qt) |
| กราฟ | matplotlib |
| ฐานข้อมูล | SQLite (`sqlite3`) |
| เรียก API | requests |
| ทดสอบ | pytest |
| CI/CD | GitHub Actions (**TODO – ยืนยันว่าตั้งค่าแล้ว**) |

## สถาปัตยกรรม

โปรเจกต์ใช้ Functional Programming Style ร่วมกับ Modular Architecture และแยกการทำงานเป็น 3 ชั้น

```text
Mini Fitness Coach
│
├── Presentation Layer
│   ├── GUI  (app.py)
│   └── CLI  (main.py)
│
├── Business Logic Layer
│   ├── Exercise Suggestion   (api.py)
│   ├── Workout Logger        (database.py)
│   └── Weekly Statistics     (analysis.py, charts.py)
│
└── Data Access Layer
    ├── ExerciseDB API        (api.py)
    └── SQLite Database       (database.py)
```

## โครงสร้างโปรเจกต์

```text
mini-fitness-coach/
├── src/
│   ├── app.py        # PySide6 desktop GUI
│   ├── main.py       # Command-line interface
│   ├── api.py        # ExerciseDB API client
│   ├── database.py   # SQLite schema, อ่าน/เขียนข้อมูล, migration
│   ├── analysis.py   # สถิติรายสัปดาห์ และ CSV export
│   └── charts.py     # กราฟรายสัปดาห์ (ใช้ร่วมกันทั้ง GUI และ CLI)
├── tests/
│   ├── test_database.py
│   └── test_main.py
├── data/
│   └── fitness.db    # สร้างอัตโนมัติ (อยู่ใน .gitignore)
├── PLAN.md / plan.md
├── README.md
├── requirements.txt
└── .gitignore
```

## การติดตั้ง

1. Clone repository แล้วเข้าโฟลเดอร์โปรเจกต์

   ```bash
   git clone https://github.com/nattakitkul/mini-fitness-coach.git
   cd mini-fitness-coach
   ```

2. (แนะนำ) สร้าง virtual environment

   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   ```

3. ติดตั้ง dependencies

   ```bash
   pip install -r requirements.txt
   ```

   ถ้า `requirements.txt` ยังไม่ครบ ให้ติดตั้งเองด้วย:

   ```bash
   pip install PySide6 matplotlib requests pytest
   ```

ต้องใช้อินเทอร์เน็ตสำหรับ Exercise Library (ข้อมูลและ GIF จาก API) ส่วนการบันทึกและดูประวัติ Workout ใช้งานแบบออฟไลน์ได้

## วิธีใช้งาน

รันจาก root ของโปรเจกต์เสมอ เพราะโค้ด import จากแพ็กเกจ `src`

**Desktop GUI**

```bash
python -m src.app
```

หน้าหลักใน Sidebar: Home, Workouts, Exercises, Progress, Records, Goals

**Command-line menu**

```bash
python -m src.main
```

เมนู: Exercise Suggestion, Workout Logger, Workout History, Weekly Performance, Exit

## ฐานข้อมูล

ไฟล์ SQLite อยู่ที่ `data/fitness.db` และถูกสร้างอัตโนมัติเมื่อเปิดโปรแกรม

| ตาราง | ความหมาย |
|-------|----------|
| `sessions` | 1 แถว = 1 ครั้งที่ไปออกกำลังกาย (`id`, `name`, `date`) |
| `sets` | 1 แถว = 1 เซ็ตจริง (`session_id`, `exercise_name`, `set_number`, `reps`, `weight`) |

เมื่อลบ session เซ็ตที่เกี่ยวข้องจะถูกลบตาม (`ON DELETE CASCADE`) ตาราง `workouts` แบบเดิมจะถูกเปลี่ยนชื่อเป็น `workouts_legacy` หลัง migration (ไม่ลบข้อมูล)

## ข้อควรรู้

- `src/api.py` ตั้ง `VERIFY_SSL = False` ตามโปรแกรมเดิม ถ้าเครือข่ายรองรับให้เปลี่ยนเป็น `True`
- ใน `src/app.py` ต้องให้ `import matplotlib.dates` เป็นบรรทัด import แรกเสมอ ไม่เช่นนั้นถ้า import PySide6 ก่อนจะเกิด `AttributeError` จาก dateutil/six
- หน้า **Home** และ **Goals** ใน GUI ยังเป็นหน้าว่างสำหรับพัฒนาต่อ
- ไฟล์ฐานข้อมูลจริงไม่ถูก commit ขึ้น Git

## ทีมพัฒนา

| ชื่อ | บทบาท | หน้าที่หลัก |
|------|-------|-------------|
| นายนันทกร โนนกลาง | Project Manager / CI-CD Integrator | วางแผน Sprint, ออกแบบ Program Flow และ Database, ดูแลเอกสาร, GitHub และ CI/CD |
| นายณัฐกิตติ์ กุลวงศ์ | Automated Tester & QA | เขียนและรัน Unit Tests, ทดสอบ API/Database/Edge Cases, หาและแก้ Bugs |
| นายวรากร โสภา | Core Developer | พัฒนา API, Exercise Suggestion, Workout Logger, Weekly Performance และเชื่อมต่อระบบ |

## เอกสารประกอบ

- [`Project Pitch.md`](Project%20Pitch.md) — ข้อเสนอโปรเจกต์
- [`plan.md`](plan.md) — แผนการพัฒนาทั้ง 4 Sprint
- `sprint1.md`, `sprint2.md`, `sprint3.md`, `final sprint.md` — รายงานผลแต่ละ Sprint

## Repository

https://github.com/nattakitkul/mini-fitness-coach