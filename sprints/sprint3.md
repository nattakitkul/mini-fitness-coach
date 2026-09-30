# Sprint 3 --- GUI Application & User Experience

## 1. Sprint Goal

เป้าหมายของ Sprint 3 คือการพัฒนา **Mini Fitness Coach** จากระบบ CLI ที่มี Core Workout Features ใน Sprint 2 ให้กลายเป็นโปรแกรมที่สามารถใช้งานผ่าน **Graphical User Interface (GUI)** ได้สะดวกมากขึ้น โดยใช้ **PySide6** เป็น Framework สำหรับพัฒนา Desktop Application

ใน Sprint นี้มุ่งเน้นการนำความสามารถที่พัฒนาไว้ใน Sprint 2 ได้แก่ **ExerciseDB API, SQLite Database, Workout Logging, Workout History และ Weekly Performance** มาเชื่อมต่อกับ GUI พร้อมเพิ่มส่วนของ Exercise Library, Exercise Detail, Workout Program, Workout Session, Records และ Progress

นอกจากนี้ยังมีการปรับปรุง User Experience ของโปรแกรม เช่น การเพิ่ม Sidebar Navigation, การแสดง Exercise เป็น Card และการแสดง GIF ของ Exercise เพื่อให้ผู้ใช้สามารถดูข้อมูลและใช้งานโปรแกรมได้ง่ายขึ้น

---

## 2. Sprint Tasks

ใน Sprint 3 ได้ดำเนินงานดังนี้

* พัฒนา Graphical User Interface ด้วย PySide6
* สร้าง Main Window สำหรับ Application
* เพิ่ม Sidebar Navigation
* เพิ่มหน้า Home
* เพิ่มหน้า Workouts
* เพิ่มหน้า Exercises
* เพิ่มหน้า Progress
* เพิ่มหน้า Records
* เพิ่มหน้า Goals
* เชื่อม Exercise Suggestion เข้ากับ GUI
* เพิ่มการเลือก Muscle Group ในหน้า Exercises
* แสดง Exercise ในรูปแบบ Exercise Card
* เพิ่มหน้า Exercise Detail
* แสดง Target Muscle และ Equipment
* แสดง Exercise Instructions
* เพิ่มการแสดง Exercise GIF
* พัฒนา Workout Program
* เพิ่ม Workout Session
* เชื่อม Workout Session กับ SQLite Database
* เพิ่ม Workout Records
* เชื่อม Weekly Performance เข้ากับ Progress Page
* เพิ่มการโหลด GIF ผ่าน Background Thread
* ทดสอบ Matplotlib กับ PySide6
* ทดสอบการทำงานของ GUI แบบ Manual
* ทดสอบ Unit Tests ด้วย Pytest
* แก้ไขปัญหาที่พบระหว่างการเชื่อมต่อ GUI กับระบบเดิม
* ใช้ Git สำหรับจัดการ Version และ Push Source Code ขึ้น GitHub

---

## 3. Main Features

### 3.1 PySide6 GUI Application

ใน Sprint 3 ได้พัฒนา GUI สำหรับ Mini Fitness Coach ด้วย **PySide6** โดยมี `app.py` เป็นส่วนหลักในการจัดการหน้าต่างและหน้าต่างย่อยของ Application

Application มี Navigation หลัก ได้แก่

```text
Home
Workouts
Exercises
Progress
Records
Goals
```

ระบบใช้ `QStackedWidget` สำหรับจัดการ Page ต่าง ๆ ทำให้ผู้ใช้สามารถเปลี่ยนหน้าการใช้งานได้จาก Sidebar โดยไม่ต้องกลับไปใช้ CLI Menu

โครงสร้างโดยรวม:

```text
Mini Fitness Coach
│
├── Home
├── Workouts
├── Exercises
├── Progress
├── Records
└── Goals
```

การพัฒนา GUI ใน Sprint นี้ทำให้ Feature ที่มีอยู่เดิมใน CLI สามารถนำมาใช้งานผ่าน Desktop Application ได้

---

### 3.2 Exercise Library

เพิ่มหน้า **Exercises** สำหรับแสดงรายการ Exercise ที่ได้จาก ExerciseDB API

ผู้ใช้สามารถเลือก Muscle Group ได้แก่

```text
Chest
Back
Legs
Shoulders
Arms
Abs
```

เมื่อเลือก Muscle Group ระบบจะเรียก:

```text
suggest_exercises()
```

จาก `api.py` เพื่อดึงข้อมูล Exercise จาก ExerciseDB API

ข้อมูลที่ได้จาก API จะถูกนำมาแสดงในรูปแบบ Exercise Card

ตัวอย่างข้อมูลที่แสดง:

```text
Exercise Name
Target Muscle
Equipment
```

ทำให้ผู้ใช้สามารถเลือก Exercise ที่ต้องการดูรายละเอียดต่อได้จาก GUI

---

### 3.3 Exercise Card และ Exercise Detail

เพิ่ม `ExerciseCard` สำหรับแสดงข้อมูล Exercise แต่ละรายการในหน้า Exercises

เมื่อผู้ใช้เลือก Exercise ระบบจะเปิดหน้า **Exercise Detail** ซึ่งแสดงข้อมูลเพิ่มเติม เช่น

* Exercise Name
* Target Muscles
* Secondary Muscles
* Equipment
* Instructions
* Exercise GIF

ตัวอย่าง:

```text
==============================
       EXERCISE DETAIL
==============================

Exercise:
Push Up

Target:
Pectorals

Equipment:
Body Weight

Secondary Muscles:
...

Instructions:
...
```

ข้อมูลดังกล่าวถูกดึงมาจากข้อมูลที่ได้รับจาก ExerciseDB API

---

### 3.4 Exercise GIF

เพิ่มการแสดง GIF ของ Exercise เพื่อช่วยให้ผู้ใช้เข้าใจลักษณะการเคลื่อนไหวของแต่ละท่าได้ง่ายขึ้น

ระบบใช้ `QMovie` ของ PySide6 สำหรับแสดง GIF และมีการสร้าง `GifLoader` ที่ใช้ `QThread` สำหรับจัดการการโหลดข้อมูลจาก Network

แนวทางการทำงาน:

```text
ExerciseDB API
      │
      ▼
    gifUrl
      │
      ▼
 HTTP Request
      │
      ▼
   GIF Data
      │
      ▼
 Temporary File
      │
      ▼
    QMovie
      │
      ▼
    GUI
```

การแยกการโหลด GIF ออกจาก GUI Thread ช่วยลดการทำงาน Network ภายใน Main Thread ของ Application

---

## 4. GUI Integration

Sprint 3 นำระบบจาก Sprint 2 มาเชื่อมต่อกับ GUI โดยไม่จำเป็นต้องสร้าง API และ Database ใหม่ทั้งหมด

โครงสร้างการทำงาน:

```text
                  PySide6 GUI
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
      Exercises     Workouts     Progress
          │            │            │
          ▼            ▼            ▼
     ExerciseDB      SQLite       SQLite
```

### 4.1 ExerciseDB Integration

หน้า Exercises เรียกใช้ Function เดิม:

```text
suggest_exercises()
```

เพื่อรับ Exercise จาก ExerciseDB API

ดังนั้นข้อมูล Exercise ใน GUI ยังคงใช้ข้อมูลจาก API เช่นเดียวกับระบบใน Sprint 2

### 4.2 SQLite Integration

Workout ที่เกิดจาก GUI สามารถส่งต่อไปยัง:

```text
log_workout()
```

เพื่อบันทึกข้อมูลลง SQLite Database

Database ยังคงใช้:

```text
data/fitness.db
```

และตาราง:

```text
workouts
```

โดยใช้ข้อมูล:

```text
exercise_name
date
sets
repetitions
weight
```

---

## 5. Workout & Exercise Integration

### 5.1 Workout Program

เพิ่มหน้า **Workouts** สำหรับแสดง Workout Program ที่เตรียมไว้

Workout Program ที่พัฒนาใน Sprint 3 ได้แก่

**Beginner Full Body**

```text
Push Up
Bodyweight Squat
Lat Pulldown
Dumbbell Shoulder Press
```

**Chest & Triceps**

```text
Bench Press
Cable Crossover
Chest Fly
Triceps Pushdown
```

**Leg Day**

```text
Barbell Squat
Leg Press
Leg Extension
Leg Curl
Calf Raise
```

ผู้ใช้สามารถเลือก Workout Program และกด Start Workout เพื่อเข้าสู่ Workout Session

---

### 5.2 Workout Session

เพิ่ม **Workout Session** สำหรับจัดการการออกกำลังกายตาม Program ที่ผู้ใช้เลือก

Flow การทำงาน:

```text
Workouts
   ↓
Select Workout Program
   ↓
Start Workout
   ↓
Workout Session
   ↓
Complete Workout
   ↓
Save Workout
```

Workout Session จะรับข้อมูล Exercise จาก Workout Program เพื่อแสดงรายการ Exercise ที่ผู้ใช้ต้องทำ

เมื่อจบ Workout ระบบสามารถบันทึกข้อมูลผ่าน:

```text
log_workout()
```

ลง SQLite Database

---

### 5.3 Workout Records

เพิ่มหน้า **Records** สำหรับดูข้อมูล Workout ที่ถูกบันทึกไว้

ระบบเรียก:

```text
get_workout_history()
```

เพื่ออ่านข้อมูลจาก SQLite

ข้อมูลที่แสดงประกอบด้วย:

```text
Date
Exercise Name
Sets
Repetitions
Weight
```

ตัวอย่าง:

```text
2026-09-30
Push Up
3 sets × 10 reps
Weight: 0 kg
```

ทำให้ผู้ใช้สามารถตรวจสอบ Workout ที่เคยบันทึกไว้จาก GUI ได้โดยไม่ต้องใช้ CLI

---

## 6. Progress & Records

### 6.1 Progress Page

เพิ่มหน้า **Progress** สำหรับแสดงสถิติการออกกำลังกายรายสัปดาห์

ระบบนำข้อมูลจาก:

```text
get_weekly_performance()
```

มาแสดงใน GUI

ข้อมูลหลัก ได้แก่:

```text
Workouts This Week
Exercises Completed
Total Sets
```

ตัวอย่าง:

```text
==============================
        WEEKLY PROGRESS
==============================

Workouts This Week: 2
Exercises Completed: 2
Total Sets: 8
```

ข้อมูลยังคงใช้หลักการคำนวณช่วง **7 วันล่าสุด** จาก Sprint 2

---

### 6.2 Weekly Sets

ระบบยังคงใช้:

```text
get_weekly_sets()
```

สำหรับดึงจำนวน Sets ในแต่ละวัน

ตัวอย่าง:

```text
Date          Total Sets

2026-09-27        8
2026-09-28        8
2026-09-29        6
```

ข้อมูลนี้สามารถนำไปใช้กับ Weekly Performance Graph ได้

---

### 6.3 Weekly Performance Graph

ระบบยังคงใช้ Matplotlib สำหรับแสดง Weekly Workout Performance

รูปแบบกราฟ:

```text
X-axis → Date
Y-axis → Total Sets
Title  → Weekly Workout Performance
```

การทำงาน:

```text
SQLite
  ↓
get_weekly_sets()
  ↓
Weekly Data
  ↓
Matplotlib
  ↓
Weekly Workout Performance
```

ระหว่าง Sprint 3 ได้มีการทดลองนำ Matplotlib Graph มา Embed ภายใน PySide6 Application ผ่าน QtAgg

อย่างไรก็ตามพบปัญหา Compatibility ใน Environment ที่ใช้พัฒนา โดยเกิด Error ระหว่าง Import Matplotlib Qt Backend

ดังนั้นการ Embed Graph แบบ QtAgg ยังถือเป็นส่วนที่ต้องปรับปรุงเพิ่มเติม และไม่ได้ถือว่าเป็น Feature ที่เสร็จสมบูรณ์ในรูปแบบ Embedded GUI

---

## 7. Testing

ใน Sprint 3 มีการทดสอบทั้งระบบเดิมและ Feature ใหม่ที่เพิ่มเข้ามา

### 7.1 Unit Testing

ยังคงใช้ **Pytest** สำหรับทดสอบส่วนของระบบที่สามารถทดสอบแบบ Automated ได้

ผลการทดสอบชุดเดิม:

```text
13 passed
```

Warnings ที่พบเกี่ยวข้องกับ Matplotlib/Qt Backend และไม่ได้ทำให้ Test ล้มเหลว

---

### 7.2 GUI Manual Testing

มีการทดสอบ Application แบบ Manual โดยตรวจสอบ Feature หลัก ได้แก่

* โปรแกรมสามารถเปิดได้
* Sidebar สามารถเปลี่ยน Page ได้
* Exercises Page สามารถแสดง Exercise ได้
* สามารถเลือก Muscle Group ได้
* Exercise Card สามารถเปิด Exercise Detail ได้
* Exercise Detail แสดงข้อมูล Exercise ได้
* Exercise GIF สามารถโหลดได้ใน Flow ที่ API ส่ง GIF URL ที่เข้าถึงได้
* Workouts Page สามารถแสดง Workout Program ได้
* สามารถเข้าสู่ Workout Session ได้
* Workout สามารถเชื่อมต่อกับ Database ได้
* Records สามารถแสดงข้อมูลจาก SQLite ได้
* Progress สามารถแสดง Weekly Statistics ได้
* Weekly Performance สามารถทำงานตาม Logic จาก Sprint 2 ได้

---

### 7.3 Issues ที่พบจากการ Testing

ระหว่างการทดสอบพบปัญหาบางส่วน ได้แก่

```text
QWindowsWindow::setGeometry:
Unable to set geometry
```

และ

```text
QThread:
Destroyed while thread is still running
```

ปัญหาแรกเกี่ยวข้องกับ Window Geometry ของ Qt ส่วนปัญหาที่สองเกี่ยวข้องกับ Lifecycle ของ Background Thread ที่ใช้ในการโหลดข้อมูล

นอกจากนี้ยังพบปัญหาการ Embed Matplotlib ผ่าน QtAgg ซึ่งทำให้ต้องแยกการแสดง Graph ออกจาก GUI ในบางกรณี

ปัญหาเหล่านี้ถูกบันทึกไว้เป็น Technical Issues สำหรับการปรับปรุงต่อไป

---

## 8. Project Structure

โครงสร้างโปรเจกต์หลังการพัฒนา GUI มีการเพิ่มส่วนของ Application และ Module ที่เกี่ยวข้องกับการพัฒนาต่อจาก Sprint 2

โครงสร้างที่ใช้ระหว่าง Sprint 3:

```text
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
│   ├── app.py
│   ├── database.py
│   ├── api.py
│   ├── analysis.py
│   └── charts.py
│
└── tests/
    ├── test_main.py
    └── test_database.py
```

หน้าที่หลักของไฟล์:

```text
app.py
→ GUI และ Application Interface

api.py
→ ExerciseDB API

database.py
→ SQLite และ Workout Data

analysis.py
→ Analysis / Performance Logic

charts.py
→ Chart / Visualization

main.py
→ CLI / Program Flow เดิม
```

Database ยังคงอยู่ใน:

```text
data/fitness.db
```

และไม่ควร Commit Database จริงขึ้น Git Repository ตามแนวทางจาก Sprint 2

---

## 9. Version Control

ใน Sprint 3 ยังคงใช้ Git และ GitHub สำหรับจัดการ Version ของ Source Code

มีการ Commit การพัฒนา GUI และ Feature ที่เกี่ยวข้องกับ Weekly Progress รวมถึงการแก้ไข Source Code ระหว่างการ Integration

Commit ที่เกี่ยวข้องกับการพัฒนา GUI ที่มีอยู่ในช่วง Sprint นี้ ได้แก่:

```text
4acfd1e Complete weekly progress GUI
```

และมีการ Push Source Code ขึ้น GitHub

Repository:

[mini-fitness-coach --- GitHub](https://github.com/nattakitkul/mini-fitness-coach)

ในระหว่างการพัฒนา Source Code มีการแก้ไขหลายส่วน เช่น:

```text
src/app.py
src/api.py
src/database.py
src/main.py
```

รวมถึงการเพิ่ม Module สำหรับ Analysis และ Charts

---

## 10. Definition of Done

Sprint 3 ถือว่าเสร็จสมบูรณ์ในส่วนของ Core GUI Features เมื่อ:

* โปรแกรมสามารถเปิด GUI ได้
* PySide6 GUI สามารถทำงานได้
* มี Main Window
* มี Sidebar Navigation
* มี Home Page
* มี Workouts Page
* มี Exercises Page
* มี Progress Page
* มี Records Page
* มี Goals Page
* Exercise Suggestion สามารถทำงานผ่าน GUI ได้
* สามารถเลือก Muscle Group ได้
* Exercise Card สามารถแสดงข้อมูล Exercise ได้
* Exercise Detail สามารถแสดงข้อมูลเพิ่มเติมได้
* สามารถแสดง Exercise GIF ได้
* มี Workout Program
* สามารถเข้าสู่ Workout Session ได้
* Workout สามารถเชื่อมต่อกับ SQLite ได้
* Records สามารถอ่านข้อมูลจาก SQLite ได้
* Progress สามารถแสดง Weekly Performance ได้
* มีการทดสอบ Unit Tests ด้วย Pytest
* Test Cases เดิมผ่านทั้งหมด 13 Tests
* มีการทดสอบ GUI แบบ Manual
* Source Code ถูกจัดการด้วย Git
* Source Code ถูก Push ขึ้น GitHub

**Technical Issues ที่ยังต้องปรับปรุง:**

* Matplotlib QtAgg ยังมี Compatibility Issue กับ Environment ที่ใช้
* การ Embed Graph ภายใน PySide6 ยังไม่สมบูรณ์
* QThread Lifecycle ยังมี Warning ในบางกรณี
* Navigation และ Workout Flow บางส่วนยังสามารถปรับปรุง User Experience ได้

---

## 11. Sprint 3 Result

หลังจบ Sprint 3 โปรแกรม **Mini Fitness Coach** ได้พัฒนาจากระบบ CLI ที่มี Core Workout Features ใน Sprint 2 มาเป็น **Desktop Application ที่มี Graphical User Interface ด้วย PySide6**

ผู้ใช้สามารถ:

1. เปิดโปรแกรมผ่าน GUI
2. เลือกหน้าใช้งานจาก Sidebar
3. เลือก Muscle Group
4. รับ Exercise Suggestion จาก ExerciseDB API
5. ดู Exercise Card
6. ดูรายละเอียด Exercise
7. ดู Equipment และ Instructions
8. ดู Exercise GIF
9. เลือก Workout Program
10. เริ่ม Workout Session
11. บันทึก Workout ลง SQLite
12. ดู Workout Records
13. ดู Weekly Progress
14. ดู Workout Count
15. ดู Exercise Frequency
16. ดู Total Sets

โครงสร้างของระบบหลัง Sprint 3 จึงสามารถสรุปได้ดังนี้:

```text
                    Mini Fitness Coach
                           │
                           ▼
                     PySide6 GUI
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
      Exercises         Workouts         Progress
          │                │                │
          ▼                ▼                ▼
     ExerciseDB         SQLite          Analysis
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                        Records
```

Sprint 3 จึงเป็น Sprint ที่เน้นการนำ **Core Features จาก Sprint 2 มาพัฒนาเป็น GUI Application** และเพิ่ม User Experience ให้สามารถใช้งาน Exercise Search, Workout, Records และ Progress ผ่านหน้าจอเดียวกันได้

อย่างไรก็ตาม จากการทดสอบยังพบ Technical Issues บางส่วน โดยเฉพาะ **Matplotlib QtAgg Compatibility และ QThread Lifecycle** ซึ่งควรนำไปพิจารณาในการพัฒนาต่อใน Sprint ถัดไป

**Sprint 3 จึงถือว่า Core GUI Features สามารถใช้งานได้ และพร้อมสำหรับการปรับปรุงด้าน Stability, Navigation และ User Experience ใน Sprint ถัดไป**.
