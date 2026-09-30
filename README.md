Project Pitch: Mini Fitness Coach
1. Project Title
Mini Fitness Coach

โปรแกรมผู้ช่วยออกกำลังกายขนาดเล็กสำหรับช่วยค้นหาท่าออกกำลังกาย บันทึกการออกกำลังกาย และดูสถิติการออกกำลังกายของผู้ใช้

2. Problem Statement
ปัจจุบันนักศึกษาหรือผู้ที่เริ่มต้นออกกำลังกายอาจไม่รู้ว่าควรเลือกท่าออกกำลังกายแบบไหนให้เหมาะกับส่วนของร่างกายที่ต้องการฝึก และเมื่อออกกำลังกายเป็นประจำก็อาจไม่มีวิธีที่ง่ายในการบันทึกว่าแต่ละวันออกกำลังกายอะไรไปบ้าง

ดังนั้นจึงต้องการสร้างโปรแกรมที่ช่วยรวบรวมข้อมูลท่าออกกำลังกายและบันทึกประวัติการออกกำลังกายไว้ในระบบ เพื่อให้ผู้ใช้สามารถค้นหาท่าออกกำลังกายและติดตามการออกกำลังกายของตัวเองได้ง่ายขึ้น

3. Proposed Solution
พัฒนาโปรแกรม Mini Fitness Coach ด้วยภาษา Python โดยเชื่อมต่อกับ Exercise API เพื่อดึงข้อมูลท่าออกกำลังกายมาแสดงให้ผู้ใช้ค้นหา

ผู้ใช้สามารถค้นหาท่าออกกำลังกายตามส่วนของร่างกายหรือกล้ามเนื้อที่ต้องการฝึก จากนั้นสามารถบันทึก Workout ของตัวเองลงในฐานข้อมูล SQLite และดูประวัติหรือสถิติการออกกำลังกายย้อนหลังได้

ระบบจะออกแบบเป็นโปรแกรมแบบ Modular และ Functional Programming Style โดยแบ่งการทำงานออกเป็นฟังก์ชันที่มีหน้าที่ชัดเจน เช่น การดึงข้อมูลจาก API การบันทึก Workout และการวิเคราะห์ข้อมูล เพื่อให้โค้ดเป็นระเบียบและสามารถพัฒนาต่อได้ง่าย

4. Domain
Health / Fitness Application

โปรเจกต์อยู่ในด้าน Health และ Fitness โดยเน้นการช่วยจัดการข้อมูลการออกกำลังกายส่วนบุคคล

5. API
API Name: ExerciseDB API (V1 Free API)
Documentation Link: https://exercisedb.dev/
Type of Data: Exercise Data เช่น Exercise Name, Body Part, Target Muscle, Equipment, Instructions และ GIF/Image
ใช้ ExerciseDB API สำหรับดึงข้อมูลท่าออกกำลังกายมาใช้ในระบบ เช่น การค้นหาและแนะนำท่าออกกำลังกายตาม Muscle Group โดยข้อมูลที่ได้รับจาก API อยู่ในรูปแบบ JSON และเรียกใช้งานผ่าน HTTP GET Request ด้วย Python requests

ระบบจะมีการจัดการกรณี API ไม่สามารถเชื่อมต่อได้ หรือได้รับข้อมูลที่ไม่ถูกต้องด้วย Exception Handling

6. Persistence Plan
ใช้ SQLite เป็นฐานข้อมูลหลักของโปรแกรม

ข้อมูลที่จัดเก็บ เช่น

Exercise

Exercise ID
Exercise Name
Body Part
Target Muscle
Equipment
Workout

Workout ID
Exercise Name
Date
Sets
Repetitions
Weight
SQLite เหมาะกับโปรเจกต์นี้เพราะสามารถเก็บข้อมูลไว้ในเครื่องและไม่จำเป็นต้องใช้ Database Server ภายนอก

นอกจากนี้สามารถเพิ่มฟังก์ชัน CSV Export เป็น Stretch Feature เพื่อให้ผู้ใช้ส่งออกประวัติ Workout ได้

7. Framework / Programming Style
ใช้ Functional Programming Style ร่วมกับ Modular Architecture

แบ่งการทำงานออกเป็นฟังก์ชันที่มีหน้าที่ชัดเจน เช่น:

fetch_exercises()
suggest_exercises()
log_workout()
get_workout_history()
analyze_weekly_performance()
show_weekly_chart()
แบ่งโค้ดออกเป็น Module เช่น:

api.py → ดึงข้อมูลจาก ExerciseDB API
database.py → จัดการ SQLite และ Workout Logs
analysis.py → วิเคราะห์ข้อมูลรายสัปดาห์
main.py → จัดการ Menu และ Program Flow
Project Architecture
Mini Fitness Coach
│
├── Presentation Layer
│   └── CLI / Menu
│
├── Business Logic Layer
│   ├── Exercise Suggestion
│   ├── Workout Logger
│   └── Weekly Statistics
│
└── Data Access Layer
    ├── Exercise API
    └── SQLite Database
8. Roles
แบ่งหน้าที่ของสมาชิกตามบทบาทดังนี้

Project Manager / CI-CD Integrator — นายนันทกร โนนกลาง

วางแผน Sprint และลำดับการพัฒนา
ออกแบบ Program Flow และ Menu
วางแผนโครงสร้าง SQLite Database
จัดทำและดูแลเอกสาร
ติดตามความคืบหน้าของทีม
จัดการ GitHub Repository และ CI/CD
Automated Tester & QA — นายณัฐกิตติ์ กุลวงศ์

เขียนและรัน Unit Tests ด้วย pytest
ทดสอบ API และ Exception Handling
ทดสอบ SQLite Database
ตรวจสอบ Edge Cases และ Invalid Inputs
ค้นหาและแก้ไข Bugs
Core Developer — นายวรากร โสภา

พัฒนาและเชื่อมต่อ ExerciseDB API
พัฒนา Exercise Suggestion
พัฒนา Workout Logger
พัฒนา Weekly Performance และ Simple Chart
เชื่อมต่อส่วนต่าง ๆ ของระบบ
9. MVP Features
MVP 1 — Exercise Suggestion by Muscle Group
ผู้ใช้สามารถเลือก Muscle Group ที่ต้องการฝึก และระบบจะแนะนำท่าออกกำลังกายที่เกี่ยวข้องจาก ExerciseDB API

ตัวอย่าง:

Select Muscle Group:

1. Chest
2. Back
3. Legs
4. Shoulders
5. Arms
6. Abs
MVP 2 — Workout Logger
ผู้ใช้สามารถบันทึก Workout ที่ทำในแต่ละวันได้

ตัวอย่างข้อมูล:

Exercise : Squat
Date     : 15/09/2026
Sets     : 3
Reps     : 10
Weight   : 40 kg
ข้อมูลจะถูกบันทึกลง SQLite และสามารถเรียกดูย้อนหลังได้

MVP 3 — Weekly Performance + Simple Chart
แสดงสถิติการออกกำลังกายของผู้ใช้ในแต่ละสัปดาห์ เช่น จำนวนครั้งที่ออกกำลังกาย จำนวน Workout และจำนวน Sets พร้อมแสดงผลในรูปแบบกราฟอย่างง่ายด้วย matplotlib

Example:

Day	Workout	Sets
Monday	Chest	4
Wednesday	Back	3
Friday	Legs	5
Sunday	Chest	4
จากข้อมูลตัวอย่าง ระบบจะสรุปว่าในสัปดาห์นั้นผู้ใช้ออกกำลังกาย 4 ครั้ง และทำทั้งหมด 16 Sets พร้อมแสดงกราฟจำนวน Sets ที่ทำในแต่ละวันด้วย matplotlib

10. Stretch Features
หลังจาก MVP เสร็จแล้ว อาจเพิ่มความสามารถดังต่อไปนี้

⭐ Favorite Exercise
ให้ผู้ใช้สามารถบันทึกท่าออกกำลังกายที่ชื่นชอบไว้ เพื่อให้สามารถเรียกดูและเลือกใช้งานได้ง่ายในภายหลัง

⭐ CSV Export
ให้ผู้ใช้สามารถส่งออกประวัติ Workout จาก SQLite Database เป็นไฟล์ CSV เพื่อนำข้อมูลไปใช้งานหรือวิเคราะห์เพิ่มเติมได้

⭐ Personal Best
บันทึกและแสดงสถิติที่ดีที่สุดของผู้ใช้ เช่น น้ำหนักสูงสุดที่เคยยกได้ในแต่ละท่าออกกำลังกาย

⭐ Monthly Statistics
เพิ่มการวิเคราะห์สถิติในระดับเดือน เช่น จำนวนวันที่ออกกำลังกาย จำนวน Workout และจำนวน Sets ในแต่ละเดือน

⭐ AI-Assisted Recommendation
เพิ่มระบบ AI เพื่อช่วยวิเคราะห์ประวัติการออกกำลังกายของผู้ใช้ และแนะนำ Workout ที่เหมาะสมกับรูปแบบการออกกำลังกายของผู้ใช้

11. Evaluation Checklist
Requirement	Plan
Python Application	✅
Public API Integration	✅ Exercise API
requests	✅
JSON Parsing	✅
SQLite Persistence	✅
Functional Programming Style	✅
Modular Functions	✅
Modular Architecture	✅
Separation of Concerns	✅
Exception Handling	✅
Unit Testing	✅ pytest
API Mock Testing	✅
Database Testing	✅
GitHub	✅
CI/CD	✅ GitHub Actions
Code Quality	✅ PEP8 / linting
CSV Export	⭐ Stretch
Data Visualization	✅ MVP 3
AI Feature	⭐ Stretch
12. Expected Outcome
เมื่อพัฒนาเสร็จ โปรแกรม Mini Fitness Coach สามารถแนะนำท่าออกกำลังกายตามกลุ่มกล้ามเนื้อจาก ExerciseDB API บันทึก Workout ลงใน SQLite และวิเคราะห์ Performance รายสัปดาห์พร้อมแสดง Simple Chart ได้

โปรเจกต์จะมีโครงสร้างแบบ Functional และ Modular พร้อม Unit Tests และ CI/CD เพื่อช่วยตรวจสอบคุณภาพของโค้ด
