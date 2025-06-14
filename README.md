1. Loyiha haqida umumiy ma'lumot
Loyiha nomi: EduPlatform Maqsad: Kundalik.com’ga o‘xshash ta'lim platformasini Python’da, OOP asosida, backend va ma'lumotlar bazasisiz, faqat sinflar va ma'lumotlarni xotirada (in-memory) saqlash orqali amalga oshirish. Platformada o‘qituvchilar, o‘quvchilar, ota-onalar va adminlar uchun funksiyalar bo‘ladi. Texnologiya: Python 3, OOP prinsiplari (inkapsulyatsiya, meros, polimorfizm, abstraksiya). Ma'lumotlar saqlanishi: Ma'lumotlar bazasi o‘rniga sinflar ichida ro‘yxatlar va lug‘atlar ishlatiladi. Foydalanuvchi rollari:
Admin: Tizimni boshqarish, foydalanuvchilarni qo‘shish/o‘chirish.
O‘qituvchi: Vazifalar berish, baho qo‘yish, dars jadvallarini tuzish.
O‘quvchi: Vazifalarni topshirish, baholarni ko‘rish.
Ota-ona: Farzandlarning o‘qish jarayonini kuzatish.
2. Kengaytirilgan modellar (Modelling)
Quyida asosiy sinflar va ularning atributlari, metodlari kengaytirilgan holda keltiriladi. Har bir sinf yanada murakkab funksiyalar va bog‘lanishlar bilan to‘ldiriladi.
AbstractRole (Abstrakt sinf, boshqa rollar uchun asos) 
Atributlar: 
_id: Unikal ID (int)
_full_name: Ism-familiya (str)
_email: Elektron pochta (str)
_password_hash: Hashlangan parol (str)
_created_at: Ro‘yxatdan o‘tgan sana (str, ISO format)
Abstrakt metodlar: 
get_profile(): Foydalanuvchi profilini qaytarish
update_profile(): Profilni yangilash
User (Foydalanuvchi sinfi, AbstractRoledan meros oladi) 
Atributlar: 
role: Foydalanuvchi roli (enum: Admin, Teacher, Student, Parent)
_notifications: Xabarnomalar ro‘yxati (list)
Metodlar: 
add_notification(message): Xabarnoma qo‘shish
view_notifications(): Xabarnomalarni ko‘rish
delete_notification(id): Xabarnomani o‘chirish
Student (O‘quvchi sinfi, Userdan meros oladi) 
Atributlar: 
grade: Sinf (masalan, “9-A”)
subjects: O‘qiydigan fanlar (lug‘at, fan nomi va o‘qituvchi IDsi)
assignments: Topshiriqlari (lug‘at: {assignment_id: status})
grades: Baholar (lug‘at: {subject: [grade1, grade2, ...]})
Metodlar: 
submit_assignment(assignment_id, content): Vazifani topshirish
view_grades(subject=None): Baholarni ko‘rish (fanga qarab filtr)
calculate_average_grade(): O‘rtacha bahoni hisoblash
Teacher (O‘qituvchi sinfi, Userdan meros oladi) 
Atributlar: 
subjects: O‘qitadigan fanlar (list)
classes: O‘qitadigan sinflar (list)
assignments: Bergan vazifalar (lug‘at: {assignment_id: Assignment})
Metodlar: 
create_assignment(title, description, deadline, subject, class_id): Vazifa yaratish
grade_assignment(assignment_id, student_id, grade): Vazifaga baho qo‘yish
view_student_progress(student_id): O‘quvchining o‘zlashtirishini ko‘rish
Parent (Ota-ona sinfi, Userdan meros oladi) 
Atributlar: 
children: Farzandlar ro‘yxati (list of Student IDs)
Metodlar: 
view_child_grades(child_id): Farzandning baholarini ko‘rish
view_child_assignments(child_id): Farzandning vazifalarini ko‘rish
receive_child_notification(child_id): Farzand haqidagi xabarnomalarni olish
Admin (Admin sinfi, Userdan meros oladi) 
Atributlar: 
permissions: Ruxsatlar ro‘yxati (list)
Metodlar: 
add_user(user): Yangi foydalanuvchi qo‘shish
remove_user(user_id): Foydalanuvchini o‘chirish
generate_report(): Tizim bo‘yicha hisobot yaratish
Assignment (Vazifa sinfi) 
Atributlar: 
id: Vazifa IDsi (int)
title: Vazifa nomi (str)
description: Tavsif (str)
deadline: Topshirish muddati (str, ISO format)
subject: Fan (str)
teacher_id: O‘qituvchi IDsi (int)
class_id: Sinf IDsi (str)
submissions: Topshirilgan javoblar (lug‘at: {student_id: content})
grades: Baholar (lug‘at: {student_id: grade})
Metodlar: 
add_submission(student_id, content): O‘quvchi javobini qo‘shish
set_grade(student_id, grade): Baho qo‘yish
get_status(): Vazifa holatini ko‘rish
Grade (Baho sinfi) 
Atributlar: 
id: Baho IDsi (int)
student_id: O‘quvchi IDsi (int)
subject: Fan (str)
value: Baho (int, 1-5)
date: Sana (str, ISO format)
teacher_id: O‘qituvchi IDsi (int)
Metodlar: 
update_grade(value): Bahoni yangilash
get_grade_info(): Baho haqida ma'lumot
Schedule (Dars jadvali sinfi) 
Atributlar: 
id: Jadval IDsi (int)
class_id: Sinf IDsi (str)
day: Hafta kuni (str)
lessons: Darslar (lug‘at: {time: {subject, teacher_id}})
Metodlar: 
add_lesson(time, subject, teacher_id): Dars qo‘shish
view_schedule(): Jadvalni ko‘rish
remove_lesson(time): Darsni o‘chirish
Notification (Xabarnoma sinfi) 
Atributlar: 
id: Xabarnoma IDsi (int)
message: Xabar matni (str)
recipient_id: Qabul qiluvchi IDsi (int)
created_at: Yaratilgan sana (str)
Metodlar: 
send(): Xabarni yuborish
mark_as_read(): O‘qilgan deb belgilash
Bog‘lanishlar:
User sinfi boshqa rollar (Student, Teacher, Parent, Admin) uchun asosiy sinf sifatida ishlatiladi.
Assignment va Grade sinflari Student va Teacher bilan bog‘lanadi.
Schedule sinfi Teacher va Student bilan bog‘lanadi.
Notification sinfi barcha rollar bilan ishlaydi.
3. Kengaytirilgan funksiyalar (Function)
Vazifalar murakkablashtirilib, quyidagi funksiyalar qo‘shildi:
Foydalanuvchi boshqaruvi: 
Foydalanuvchi ro‘yxatdan o‘tish, parolni shifrlash (oddiy hash funksiyasi).
Rolga qarab cheklovlar (masalan, faqat admin foydalanuvchi qo‘sha oladi).
Profilga qo‘shimcha ma'lumotlar (telefon, manzil).
Vazifalar tizimi: 
Vazifalarga qiyinchilik darajasi qo‘shish (masalan, “o‘rta”, “qiyin”).
Vazifalarni guruhlarga bo‘lish (masalan, sinf yoki guruh bo‘yicha).
Vazifa topshirishda fayl hajmi va formatini tekshirish.
Baholar tizimi: 
Baholarni statistik tahlil qilish (o‘rtacha, eng yuqori, eng past).
Baholarga izoh qo‘shish imkoniyati.
O‘quvchilar uchun baholar tarixini ko‘rish.
Dars jadvali: 
Dars jadvalida konfliktlarni tekshirish (masalan, bir vaqtda ikki dars).
Haftalik va oylik jadvallarni ko‘rish.
O‘qituvchi bandligini hisobga olish.
Xabarnoma tizimi: 
Avtomatik xabarnomalar (masalan, vazifa muddati yaqinlashganda).
Xabarnomalarni filtr qilish (o‘qilmagan, muhim).
Ota-onalarga maxsus xabarlar (farzandning bahosi past bo‘lsa).
Hisobotlar: 
O‘quvchilarning fanlar bo‘yicha muvaffaqiyat grafigi.
O‘qituvchilarning ish yuki tahlili.
Sinf bo‘yicha umumiy statistika.
4. Kengaytirilgan ma'lumotlar (Data)
Ma'lumotlar backend’siz, sinflar ichida saqlanadi. Quyidagi jadvallar tuzilmasi simulyatsiya qilinadi:
Users (Foydalanuvchilar): 
id, full_name, email, password_hash, role, created_at, phone, address
Students (O‘quvchilar): 
user_id, grade, subjects (lug‘at: {subject: teacher_id}), assignments (lug‘at), grades (lug‘at)
Teachers (O‘qituvchilar): 
user_id, subjects, classes, workload (o‘qitish soatlari)
Parents (Ota-onalar): 
user_id, children (list of Student IDs), notification_preferences (lug‘at)
Assignments (Vazifalar): 
id, title, description, deadline, subject, teacher_id, class_id, difficulty, submissions, grades
Grades (Baholar): 
id, student_id, subject, value, date, teacher_id, comment
Schedules (Dars jadvallari): 
id, class_id, day, lessons (lug‘at: {time: {subject, teacher_id}})
Notifications (Xabarnomalar): 
id, message, recipient_id, created_at, is_read, priority
Ma'lumotlar oqimi:
Foydalanuvchi qo‘shiladi → Users ro‘yxatiga yoziladi.
O‘qituvchi vazifa yaratadi → Assignments ro‘yxatiga qo‘shiladi → O‘quvchi va ota-onalarga xabarnoma yuboriladi.
O‘quvchi vazifa topshiradi → submissions lug‘atiga yoziladi → O‘qituvchi baho qo‘yadi → Grades ro‘yxatiga qo‘shiladi.

Qo‘shimcha funksiyalar:
Vazifa muddati monitoringi: Vazifa muddati o‘tgan bo‘lsa, avtomatik ravishda “kech topshirildi” deb belgilash.
Statistik tahlil: O‘quvchilarning fanlar bo‘yicha o‘rtacha bahosini hisoblash va eng yaxshi o‘quvchilarni aniqlash.
Dars jadvali optimallashtirish: O‘qituvchilarning bandligiga qarab jadval tuzishda konfliktlarni oldini olish.
Xavfsizlik: Oddiy parol shifrlash (hashlib yordamida) va foydalanuvchi autentifikatsiyasi.
Murakkab tasklar:
Vazifa topshirishda cheklovlar: O‘quvchi faqat belgilangan muddat ichida va to‘g‘ri formatda (masalan, matn uzunligi 500 belgidan oshmasligi) vazifa topshira oladi.
Baholar tahlili: Har bir o‘quvchi uchun fan bo‘yicha o‘rtacha baho, eng yuqori va eng past baholarni hisoblash.
Jadval optimallashtirish: Bir o‘qituvchi bir vaqtda faqat bitta sinfga dars o‘ta oladi.
Xabarnoma prioritizatsiyasi: Muhim xabarnomalar (masalan, past baholar) birinchi navbatda ko‘rsatiladi.
Hisobot generatsiyasi: Admin uchun barcha o‘quvchilarning o‘zlashtirish darajasini CSV formatida eksport qilish imkoniyati.


So’ngra barcha malumotlarni .XLSX, CSV va SSMS ga qoshib chiqish kerak boladi 

 export_to_xlsx(): Ma'lumotlarni .xlsx fayliga saqlash. 
export_to_csv(): Ma'lumotlarni .csv fayliga saqlash. 
export_to_sql(): Ma'lumotlarni SSMS uchun SQL INSERT      so‘rovlariga aylantirish.

.xlsx: Har bir jadval uchun alohida varaq (sheet). 
.csv: Har bir jadval uchun alohida fayl. 
SSMS: Har bir jadval uchun CREATE TABLE va INSERT INTO so‘rovlar.
Ma'lumotlarni birdaniga eksport qilish: Har bir foydalanuvchi, vazifa yoki baho qo‘shilganda avtomatik .xlsx, .csv va SQL fayllariga saqlash. 
Eksport optimallashtirish: Fayl hajmini cheklash uchun faqat yangi yoki o‘zgartirilgan ma'lumotlarni eksport qilish. 
Ma'lumotlar validatsiyasi: Eksport qilishdan oldin ma'lumotlarni tekshirish (masalan, bo‘sh maydonlar yo‘qligi). 
SQL jadvallarida cheklovlar: SSMS uchun jadvallarda PRIMARY KEY, FOREIGN KEY va CHECK cheklovlari qo‘llaniladi. 
Eksport jurnali: Har bir eksport amaliyoti uchun log yozish (qachon, qaysi formatda saqlangan).
