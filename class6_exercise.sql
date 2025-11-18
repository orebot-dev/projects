create database class6_exercise

use class6_exercise;

create table student
(student_id int(9) primary key,
 FIRST_NAME varCHAR(15), 
 LAST_NAME VARCHAR(15), 
 college_years int(1),
 enrollment_studentyear int(4),
 major varchar(100),
 gpa decimal(3,2),
 college varchar(100) default 'college of business');
 
select * from student;

 insert into student
 values 
 ('123456789 ','Kynon','Sell',4,2025,null,4.0, default);
 
 insert into student
 values 
 ('98765','xyz','abc',4,2025,'ISOM',4.0, default);
 
 update student
 set college = 'college of Art'
 where student_id = 98765;
 
 create table enrollment
 (Enrollment_id int(9) primary key,
 student_id int,
 course_id varchar(10) default 'BIS413');
 
alter table enrollment add constraint foreign key (student_id) references student(student_id)
 
 