# Sprint 2 --- Core Workout Features

## 1. Sprint Goal

เป้าหมายของ Sprint 2 คือการพัฒนา **Mini Fitness Coach** จาก CLI Prototype
ใน Sprint 1 ให้สามารถทำงานเป็นโปรแกรมบันทึกและติดตามการออกกำลังกายได้จริง
โดยเพิ่มการเชื่อมต่อ **ExerciseDB API**, การจัดเก็บข้อมูลด้วย **SQLite**,
การบันทึกและดูประวัติ Workout, การคำนวณสถิติ Weekly Performance
และการแสดงผลข้อมูลในรูปแบบกราฟ

------------------------------------------------------------------------

## 2. Sprint Tasks

ใน Sprint 2 ได้ดำเนินงานดังนี้

-   เชื่อมต่อ ExerciseDB API สำหรับแนะนำท่าออกกำลังกาย
-   เพิ่มการเลือก Exercise ตาม Muscle Group
-   สร้าง SQLite Database สำหรับจัดเก็บข้อมูล Workout
-   สร้างตาราง `workouts`
-   พัฒนา Workout Logger ให้บันทึกข้อมูลลง Database
-   พัฒนา Workout History สำหรับดูประวัติการออกกำลังกาย
-   พัฒนา Weekly Performance สำหรับคำนวณสถิติ
-   เพิ่มการคำนวณ Workout Count
-   เพิ่มการคำนวณ Exercise Frequency
-   เพิ่มการคำนวณ Total Sets
-   พัฒนา Weekly Performance Graph ด้วย Matplotlib
-   เพิ่มฟังก์ชันสำหรับดึงจำนวน Sets ของแต่ละวันในช่วง 7 วันล่าสุด
-   สร้างและปรับปรุง Unit Tests ด้วย Pytest
-   ตรวจสอบการทำงานของโปรแกรมแบบ Manual
-   ใช้ Git สำหรับจัดการ Version และ Push Source Code ขึ้น GitHub

------------------------------------------------------------------------

## 3. Main Features

### 3.1 Exercise Suggestion + ExerciseDB API

ใน Sprint 2 ระบบ Exercise Suggestion ถูกพัฒนาจากโครงสร้างเมนูใน Sprint 1
ให้สามารถดึงข้อมูล Exercise จาก **ExerciseDB API** ได้จริง

ผู้ใช้สามารถเลือก Muscle Group ได้แก่

-   Chest
-   Back
-   Legs
-   Shoulders
-   Arms
-   Abs

ระบบจะส่ง Request ไปยัง API และแสดงรายการ Exercise ที่เกี่ยวข้อง พร้อมข้อมูล
Equipment

ตัวอย่างการทำงาน:

``` text
1. Exercise Suggestion

Select Muscle Group:
1. Chest
2. Back
3. Legs
4. Shoulders
5. Arms
6. Abs
7. Back to Main Menu
```

ระบบรองรับการ Map Muscle Group ไปยัง Body Part ที่ API ใช้งาน เช่น

``` text
Chest    → chest
Back     → back
Legs     → upper legs, lower legs
Shoulders → shoulders
Arms     → upper arms, lower arms
Abs      → waist
```

------------------------------------------------------------------------

### 3.2 SQLite Database

เพิ่มระบบ Database ด้วย **SQLite** เพื่อจัดเก็บข้อมูล Workout แบบถาวร

Database:

``` text
data/fitness.db
```

สร้างตาราง:

``` text
workouts
```

โครงสร้างข้อมูล:

``` text
id
exercise_name
date
sets
repetitions
weight
```

ตัวอย่าง:

``` text
exercise_name = Bench Press
date          = 2026-09-28
sets          = 4
repetitions   = 10
weight        = 20
```

การสร้าง Database ใช้ฟังก์ชัน:

``` text
create_database()
```

------------------------------------------------------------------------

### 3.3 Workout Logger

Workout Logger ถูกพัฒนาให้สามารถบันทึกข้อมูลลง SQLite Database ได้จริง

ข้อมูลที่รับจากผู้ใช้ ได้แก่

-   Exercise Name
-   Date
-   Sets
-   Repetitions
-   Weight

เมื่อผู้ใช้กรอกข้อมูลครบ ระบบจะเรียก:

``` text
log_workout()
```

เพื่อบันทึกข้อมูลลงตาราง `workouts`

------------------------------------------------------------------------

### 3.4 Workout History

เพิ่มเมนู **Workout History** สำหรับแสดงข้อมูล Workout ที่ถูกบันทึกไว้ใน Database

ระบบเรียก:

``` text
get_workout_history()
```

เพื่อดึงข้อมูลจากตาราง `workouts`

ข้อมูลที่แสดงประกอบด้วย:

-   Exercise Name
-   Date
-   Sets
-   Repetitions
-   Weight

------------------------------------------------------------------------

### 3.5 Weekly Performance

พัฒนา Weekly Performance จากโครงสร้างใน Sprint 1 ให้สามารถคำนวณข้อมูลจาก
Database ได้จริง

ระบบแสดงข้อมูลหลัก ได้แก่

``` text
Workout Count
Exercise Frequency
Total Sets
```

โดยใช้ข้อมูล Workout ในช่วง **7 วันล่าสุด** หรือวันนี้รวมย้อนหลัง 6 วัน

ฟังก์ชันหลัก:

``` text
get_weekly_performance()
```

ตัวอย่าง:

``` text
==============================
      WEEKLY PERFORMANCE
==============================

Workout count: 2
Exercise frequency: 1
Total sets: 8
```

------------------------------------------------------------------------

### 3.6 Weekly Performance Graph

เพิ่มกราฟสำหรับแสดงจำนวน Sets ที่ทำได้ในแต่ละวันที่มี Workout ในช่วง 7 วันล่าสุด

ฟังก์ชันที่ใช้:

``` text
get_weekly_sets()
show_weekly_chart()
```

ระบบใช้ **Matplotlib** ในการสร้าง Bar Chart

กราฟประกอบด้วย:

-   X-axis → Date
-   Y-axis → Total Sets
-   Title → Weekly Workout Performance

เมื่อผู้ใช้เลือก Weekly Performance โปรแกรมจะเปิดหน้าต่างกราฟเพื่อแสดงข้อมูล

------------------------------------------------------------------------

## 4. API Integration

Sprint 2 เพิ่มการเชื่อมต่อกับ ExerciseDB API โดยใช้ Python `requests`

API ที่ใช้งาน:

``` text
https://oss.exercisedb.dev/api/v1/exercises/bodyparts
```

ระบบรองรับการส่ง Body Part ที่ต้องการและจำกัดจำนวนผลลัพธ์ที่แสดง

ตัวอย่าง:

``` text
bodyParts=chest
limit=25
```

ในส่วนของ API มีการจัดการกรณี Request ไม่สำเร็จและ Timeout
เพื่อไม่ให้โปรแกรมหยุดทำงานโดยไม่แสดงข้อความที่เหมาะสม

------------------------------------------------------------------------

## 5. Database Functions

ฟังก์ชันหลักที่เพิ่มใน Sprint 2 ได้แก่

``` text
create_database()
log_workout()
get_workout_history()
get_weekly_performance()
get_weekly_sets()
```

หน้าที่ของแต่ละฟังก์ชัน:

  Function                     หน้าที่
  ---------------------------- -----------------------------------
  `create_database()`          สร้าง Database และตาราง `workouts`
  `log_workout()`              บันทึก Workout
  `get_workout_history()`      ดึงประวัติ Workout
  `get_weekly_performance()`   คำนวณสถิติ 7 วันล่าสุด
  `get_weekly_sets()`          ดึงจำนวน Sets แยกตามวันที่

------------------------------------------------------------------------

## 6. Testing

ใช้ **Pytest** สำหรับทดสอบ Database และ Main Application

หลังพัฒนา Sprint 2 มี Test Cases รวมทั้งหมด:

``` text
13 tests
```

ผลการทดสอบล่าสุด:

``` text
13 passed, 8 warnings in 8.59s
```

Warnings ที่พบเป็น `DeprecationWarning` จาก Matplotlib/Qt Backend
และไม่ได้ทำให้ Test ล้มเหลว

ดังนั้น Test Cases ทั้งหมดสามารถทำงานผ่านได้

------------------------------------------------------------------------

## 7. Manual Testing

มีการทดสอบการใช้งานจริงของโปรแกรม โดยตรวจสอบว่า:

-   โปรแกรมสามารถ Run ได้
-   Exercise Suggestion สามารถดึงข้อมูลจาก API ได้
-   สามารถเลือก Muscle Group ได้
-   Workout Logger สามารถบันทึกข้อมูลลง SQLite ได้
-   Workout History สามารถแสดงข้อมูลที่บันทึกไว้ได้
-   Weekly Performance สามารถคำนวณสถิติได้
-   Weekly Performance สามารถเปิดกราฟได้
-   กราฟแสดงจำนวน Sets ตามวันที่ได้

ตัวอย่างการทดสอบ Graph พบว่าโปรแกรมสามารถเปิดหน้าต่าง **Figure 1** และแสดง
Weekly Workout Performance ได้สำเร็จ

------------------------------------------------------------------------

## 8. Project Structure

โครงสร้างโปรเจกต์หลังจบ Sprint 2:

``` text
mini-fitness-coach/

│
├── PLAN.md
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   └── fitness.db
│
├── src/
│   ├── main.py
│   ├── database.py
│   └── api.py
│
└── tests/
    ├── test_main.py
    └── test_database.py
```

หมายเหตุ:

`data/` ถูกเพิ่มไว้ใน `.gitignore` เพื่อไม่ให้ไฟล์ Database ที่สร้างจากการใช้งานจริงถูก
Commit ขึ้น Git Repository

------------------------------------------------------------------------

## 9. Version Control

ใช้ Git สำหรับจัดการ Version ของโปรเจกต์ และใช้ GitHub เป็นพื้นที่จัดเก็บ Source
Code

Commit สำคัญใน Sprint 2 ได้แก่:

``` text
3a00d94 Add weekly performance
39874e5 Add weekly performance chart
```

Commit ล่าสุดของ Sprint 2:

``` text
39874e5 Add weekly performance chart
```

และ Push ขึ้น GitHub สำเร็จแล้ว

Repository:

[mini-fitness-coach ---
GitHub](https://github.com/nattakitkul/mini-fitness-coach)

------------------------------------------------------------------------

## 10. Definition of Done

Sprint 2 ถือว่าเสร็จสมบูรณ์เมื่อ:

-   โปรแกรมสามารถ Run ได้
-   Exercise Suggestion เชื่อมต่อ ExerciseDB API ได้
-   สามารถเลือก Muscle Group และรับ Exercise Suggestion ได้
-   SQLite Database สามารถสร้างได้
-   Workout Logger สามารถบันทึกข้อมูลลง Database ได้
-   Workout History สามารถแสดงข้อมูลจาก Database ได้
-   Weekly Performance สามารถคำนวณ Workout Count ได้
-   Weekly Performance สามารถคำนวณ Exercise Frequency ได้
-   Weekly Performance สามารถคำนวณ Total Sets ได้
-   Weekly Performance Graph สามารถแสดงผลได้
-   Unit Tests ด้วย Pytest ผ่านทั้งหมด
-   Pytest ผ่านทั้งหมด 13 Tests
-   Manual Testing ของ Graph ผ่าน
-   Source Code ถูก Commit และ Push ขึ้น GitHub
-   Database ไม่ถูก Commit ขึ้น Git Repository

------------------------------------------------------------------------

## 11. Sprint 2 Result

หลังจบ Sprint 2 โปรแกรมพัฒนาจาก **CLI Prototype** ใน Sprint 1
มาเป็นโปรแกรมที่สามารถใช้งานฟังก์ชันหลักของ **Mini Fitness Coach** ได้จริง

ผู้ใช้สามารถ:

1.  เลือก Muscle Group
2.  รับ Exercise Suggestion จาก ExerciseDB API
3.  บันทึก Workout
4.  เก็บข้อมูล Workout ใน SQLite
5.  ดู Workout History
6.  ดูสถิติการออกกำลังกายในช่วง 7 วันล่าสุด
7.  ดูกราฟ Weekly Workout Performance

ผลการทดสอบล่าสุด:

``` text
13 passed
```

Sprint 2 จึงถือว่า **Complete** และพร้อมเข้าสู่ขั้นตอน User Acceptance Testing
(UAT) ก่อนเริ่ม Sprint ถัดไป
