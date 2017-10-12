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

create table weather(
	`date`DATE,
	`time` char(128),
	`city` char(128),
	`cityIndex` int,
	`temperature` double
)
