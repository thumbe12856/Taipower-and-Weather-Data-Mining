create table test(
`id` int NOT NULL AUTO_INCREMENT,
`date`DATE,
`time` char(128),
`northSupply` DOUBLE,
`northUsage` DOUBLE,
`centerSupply` DOUBLE,
`centerUsage` DOUBLE,
`southSupply` DOUBLE,
`southUsage` DOUBLE,
`eastSupply` DOUBLE,
`eastUsage` DOUBLE,
PRIMARY KEY (id)
)

select test.date, MAX(test.northSupply) from `test` where date < '2017/6/31' group by test.date;
select test.date, MAX(test.northUsage) from `test` where date < '2017/6/31' group by test.date;
select test.date, MAX(test.centerSupply) from `test` where date < '2017/6/31' group by test.date;
select test.date, MAX(test.centerUsage) from `test` where date < '2017/6/31' group by test.date;
select test.date, MAX(test.southSupply) from `test` where date < '2017/6/31' group by test.date;
select test.date, MAX(test.southUsage) from `test` where date < '2017/6/31' group by test.date;
select test.date, MAX(test.eastSupply) from `test` where date < '2017/6/31' group by test.date;
select test.date, MAX(test.eastUsage) from `test` where date < '2017/6/31' group by test.date;
