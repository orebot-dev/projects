create database Homework2_413

use Homework2_413

create table employees
(employee_id int(9) primary key,
 employee_first_name varchar(20),
 employee_last_name varchar(20),
 DOB Date,
 street char(20),
 city char(15),
 state char(2),
 zip int(5),
 projects_assigned int(2));
 
   insert into employees
  values('123456789', 'bob', 'baker','2000-05-07','123 newton','Muncie','in',47822,2);
  
  insert into employees
  values('191385601', 'bilbo', 'baggins','1999-04-09','456 mckinly','Yorktown','in',46123,2);

insert into employees
values('019181714', 'Hugh', 'Jaynus','2003-04-03', '456 brighton','Fishers','in',12345,0);

update employees
set city = 'anchorage'
where employee_id ='123456789';

update employees
set state ='ak'
where employee_id = '123456789';

CREATE TABLE project (
  project_id INT(9) PRIMARY KEY,
  project_title varchar(20),
  project_start date,
  project_end date,
  Employees_working int(2),
  FOREIGN key (Employees_working) References employees(employee_id));
  
  
  insert into project
  values('131146678','mckinley cleanup','2025-10-17','2025-12-10','123456789');
  
  INSERT INTO project
  values('999944444','Bethal ave roadwork','2025-10-18','2090-12-10','123456789');
  
  insert into project 
  values('113367981', 'Wheeling ave pickup','2025-10-17','2025-10-17','191385601');
  
  insert into project
  values('120987136','Tillotson roadwork','2025-10-20','2099-12-10','191385601');
  
  update project
set state ='ak'
where employee_id = '123456789';

select project_id
from project
where project_id='120987136'

select first_name
from employee
where employee_id = '120987136'

 