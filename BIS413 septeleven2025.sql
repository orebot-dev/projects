create database class5_relationships
use class5_relationships;

select * from customers;
select * from orders;

describe customers;

alter table customers modify CID CHAR (4);
alter table customers add primary key (CID);

alter table orders modify orderid CHAR (4);
alter table orders add primary key (orderid);

alter table orders modify CID CHAR (4);
alter table orders add constraint foreign key (CID) references customers(CID);