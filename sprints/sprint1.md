# Sprint 1 — CLI Interface & Input Validation

## 1. Sprint Goal

เป้าหมายของ Sprint 1 คือการพัฒนาโครงสร้างพื้นฐานของโปรแกรม **Mini Fitness Coach** โดยเริ่มจากส่วนติดต่อผู้ใช้ผ่าน Command Line Interface (CLI) ให้ผู้ใช้สามารถเลือกเมนูหลัก เข้าใช้งานแต่ละฟังก์ชัน และกรอกข้อมูลพื้นฐานได้อย่างถูกต้อง รวมถึงมีการตรวจสอบ Input และทดสอบการทำงานด้วย Pytest

---

## 2. Sprint Tasks

ใน Sprint 1 ได้ดำเนินงานดังนี้

* สร้างโครงสร้างโปรเจกต์ Python
* สร้าง Main Menu
* สร้าง Exercise Suggestion Menu
* สร้าง Workout Logger Menu
* สร้าง Weekly Performance Menu
* เพิ่มการตรวจสอบ Main Menu Choice
* เพิ่มการตรวจสอบ Exercise Menu Choice
* เพิ่มการตรวจสอบรูปแบบวันที่
* จัดการกรณีผู้ใช้กรอกข้อมูลไม่ถูกต้อง
* สร้าง Unit Tests ด้วย Pytest
* ตรวจสอบการทำงานของโปรแกรมและแก้ไขข้อผิดพลาด
* ใช้ Git สำหรับจัดเก็บ Version ของโปรเจกต์และ Push ขึ้น GitHub

---

## 3. Main Features

### 3.1 Main Menu

สร้างเมนูหลักสำหรับให้ผู้ใช้เลือกฟังก์ชันของโปรแกรม ได้แก่

1. Exercise Suggestion
2. Workout Logger
3. Weekly Performance
4. Exit

หากผู้ใช้กรอกตัวเลือกที่ไม่ถูกต้อง โปรแกรมจะแจ้งเตือนและให้เลือกใหม่

---

### 3.2 Exercise Suggestion

สร้างเมนูสำหรับเลือก Muscle Group ที่ผู้ใช้ต้องการ ได้แก่

* Chest
* Back
* Legs
* Shoulders
* Arms
* Abs

ใน Sprint 1 ระบบยังเป็นโครงสร้างพื้นฐานของเมนู โดยการดึงข้อมูล Exercise จาก API จะพัฒนาเพิ่มเติมใน Sprint ถัดไป

---

### 3.3 Workout Logger

สร้างเมนูสำหรับรับข้อมูลการออกกำลังกายจากผู้ใช้ ได้แก่

* Exercise Name
* Date
* Sets
* Repetitions
* Weight

มีการตรวจสอบรูปแบบวันที่ด้วยฟังก์ชัน `is_valid_date()` โดยกำหนดรูปแบบเป็น `YYYY-MM-DD`

หากวันที่ไม่ถูกต้อง ระบบจะแจ้งเตือนและให้ผู้ใช้กรอกใหม่

---

### 3.4 Weekly Performance

สร้างโครงสร้างเบื้องต้นสำหรับแสดงข้อมูลสถิติการออกกำลังกาย ได้แก่

* Workout Count
* Exercise Frequency
* Total Sets
* Chart

ใน Sprint 1 ส่วนนี้ยังเป็นเพียงโครงสร้างของเมนู โดยการคำนวณข้อมูลจริงและสร้างกราฟจะพัฒนาใน Sprint ถัดไป

---

## 4. Input Validation

มีการสร้างฟังก์ชันสำหรับตรวจสอบ Input ได้แก่

```text
is_valid_menu_choice()
is_valid_exercise_choice()
is_valid_date()
```

ตัวอย่างการตรวจสอบวันที่:

```text
2026-09-22 → Valid
2026-13-50 → Invalid
abc → Invalid
22-09-2026 → Invalid
```

การตรวจสอบ Input ช่วยป้องกันไม่ให้โปรแกรมทำงานผิดพลาดเมื่อผู้ใช้กรอกข้อมูลที่ไม่ตรงตามรูปแบบที่กำหนด

---

## 5. Testing

ใช้ **Pytest** สำหรับทดสอบฟังก์ชันและเมนูหลักของโปรแกรม

มี Test Cases ทั้งหมด 9 รายการ ได้แก่

1. Test Main Menu
2. Test Exercise Menu
3. Test Workout Logger
4. Test Weekly Performance
5. Test Invalid Main Menu Choice
6. Test Main Menu Choice Validation
7. Test Exercise Menu Choice Validation
8. Test Invalid Exercise Choice
9. Test Date Validation

ผลการทดสอบ:

```text
9 passed in 0.07s
```

ดังนั้น Test Cases ที่สร้างใน Sprint 1 สามารถทำงานผ่านทั้งหมด

---

## 6. Project Structure

โครงสร้างเบื้องต้นของโปรเจกต์:

```text
mini-fitness-coach/
│
├── PLAN.md
├── README.md
├── requirements.txt
│
├── data/
│
├── src/
│   └── main.py
│
└── tests/
    └── test_main.py
```

---

## 7. Version Control

ใช้ Git สำหรับจัดการ Version ของโปรเจกต์ และใช้ GitHub เป็นพื้นที่จัดเก็บ Source Code

Sprint 1 ได้ทำการ Commit และ Push Source Code ขึ้น GitHub เรียบร้อยแล้ว

Repository:

[mini-fitness-coach — GitHub](https://github.com/nattakitkul/mini-fitness-coach?utm_source=chatgpt.com)

---

## 8. Definition of Done

Sprint 1 ถือว่าเสร็จสมบูรณ์เมื่อ:

* โปรแกรมสามารถ Run ได้
* Main Menu ทำงานได้
* สามารถเข้าแต่ละเมนูได้
* สามารถกลับจาก Exercise Menu ได้
* Invalid Menu Choice ไม่ทำให้โปรแกรม Crash
* Exercise Menu มีการตรวจสอบ Input
* Workout Logger มีการตรวจสอบวันที่
* ฟังก์ชันมีหน้าที่ชัดเจน
* มี Unit Tests ด้วย Pytest
* Pytest ผ่านทั้งหมด 9 Tests
* Source Code ถูกจัดเก็บบน GitHub

---

## 9. Sprint 1 Result

หลังจบ Sprint 1 โปรแกรมสามารถทำงานในระดับ **CLI Prototype** โดยผู้ใช้สามารถเลือกเมนูหลัก เลือก Muscle Group และกรอกข้อมูล Workout ได้ พร้อมมีระบบตรวจสอบ Input และ Unit Testing

ส่วนการเชื่อมต่อ **ExerciseDB API**, การบันทึกข้อมูลลง **SQLite**, การวิเคราะห์ข้อมูล และการสร้างกราฟ จะเป็นงานหลักของ Sprint ถัดไป
