create database BIS413
use bis413;

drop table rep;


create table rep 
(rep_num char(2) primary key,
last_name varchar(15), 
first_name varchar(15),
street varchar(15), 
city varchar(15), 
state char(2), 
zip char(5), 
commission decimal(7,2), 
rate decimal(3,2) );




INSERT INTO REP
VALUES
('20','Kaiser','Valerie','624 Randall','Grove','FL', '33321',20542.50,0.05);
INSERT INTO REP
VALUES
('35','Hull','Richard','532 Jackson','Sheldon','FL', '33553',39216.00,0.07);

INSERT INTO REP (REP_NUM, LAST_NAME, FIRST_NAME)
VALUES
('36','O''Toole','Tina');

SELECT * FROM REP;

INSERT INTO REP
VALUES
('22', NULL, 'NULL', '624 Randall','Grove','FL', '33321',20542.50,0.05);

UPDATE REP
SET LAST_NAME = 'Perry'
WHERE REP_NUM = '35';

DELETE FROM REP
WHERE REP_NUM = '45';


alter table rep add column email varchar(1000);
	
alter table rep drop column email;

alter table rep modify column zip int;

alter table rep modify column zip char(4); 


drop table rep;
CREATE TABLE REP
(REP_NUM CHAR(2) PRIMARY KEY,
LAST_NAME CHAR(15) NOT NULL,
FIRST_NAME CHAR(15) NOT NULL,
STREET CHAR(15),
CITY CHAR(15),
STATE CHAR(2),
ZIP CHAR(5),
COMMISSION DECIMAL(7,2),
RATE DECIMAL(3,2) );

CREATE TABLE CUSTOMER
(CUSTOMER_NUM CHAR(3) PRIMARY KEY,
CUSTOMER_NAME CHAR(35) NOT NULL,
STREET CHAR(15),
CITY CHAR(15),
STATE CHAR(2),
ZIP CHAR(5),
BALANCE DECIMAL(8,2),
CREDIT_LIMIT DECIMAL(8,2),
REP_NUM CHAR(2) );

CREATE TABLE ORDERS
(ORDER_NUM CHAR(5) PRIMARY KEY,
ORDER_DATE DATE,
CUSTOMER_NUM CHAR(3) );

INSERT INTO REP
VALUES
('20','Kaiser','Valerie','624 Randall','Grove', 'FL','33321',20542.50,0.05);

INSERT INTO REP
VALUES
('35','Hull','Richard','532 Jackson','Sheldon', 'FL','33553',39216.00,0.07);

INSERT INTO REP
VALUES
('65','Perez','Juan','1626 Taylor','Fillmore', 'FL','33336',23487.00,0.05);

INSERT INTO CUSTOMER
VALUES
('148','Al''s Appliance and Sport','2837 Greenway','Fillmore','FL','33336',6550.00,7500.00,'20');
INSERT INTO CUSTOMER
VALUES
('282','Brookings Direct','3827 Devon','Grove','FL','33321',431.50,10000.00,'35');
INSERT INTO CUSTOMER
VALUES
('356','Ferguson''s','382 Wildwood','Northfield','FL','33146',5785.00,7500.00,'65');
INSERT INTO CUSTOMER
VALUES
('408','The Everything Shop','1828 Raven','Crystal','FL','33503',5285.25,5000.00,'35');
INSERT INTO CUSTOMER
VALUES
('462','Bargains Galore','3829 Central','Grove','FL','33321',3412.00,10000.00,'65');

INSERT INTO CUSTOMER
VALUES
('524','Kline''s','838 Ridgeland','Fillmore','FL','33336',12762.00,15000.00,'20');
INSERT INTO CUSTOMER
VALUES
('608','Johnson''s Department Store','372 Oxford','Sheldon','FL','33553',2106.00,10000.00,'65');
INSERT INTO CUSTOMER
VALUES
('687','Lee''s Sport and Appliance','282 Evergreen','Altonville','FL','32543',2851.00,5000.00,'35');
INSERT INTO CUSTOMER
VALUES
('725','Deerfield''s Four Seasons','282 Columbia','Sheldon','FL','33553',248.00,7500.00,'35');
INSERT INTO CUSTOMER
VALUES
('842','All Season','28 Lakeview','Grove','FL','33321',8221.00,7500.00,'20');

INSERT INTO ORDERS
VALUES
('21608','2007-10-20','148');
INSERT INTO ORDERS
VALUES
('21610','2007-10-20','356');
INSERT INTO ORDERS
VALUES
('21613','2007-10-21','408');
INSERT INTO ORDERS
VALUES
('21614','2007-10-21','282');
INSERT INTO ORDERS
VALUES
('21617','2007-10-23','608');
INSERT INTO ORDERS
VALUES
('21619','2007-10-23','148');
INSERT INTO ORDERS
VALUES
('21623','2007-10-23','608');

select FIRST_NAME,LAST_NAME
from rep
where rep_num = '35';

select order_num
from orders
where customer_num = '608';

select order_date
from orders
where order_num = '21617' or order_num = '21623';

SELECT
customer_num,
customer_name,
(credit_limit-balance) AS Available_Credit
FROM customer
WHERE (credit_limit-balance) >= 5000;

select *
from customer
where state != 'FL';

