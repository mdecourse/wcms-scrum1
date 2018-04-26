drop table if exists entries;
create table entries(
	id integer primary key autoincrement,
	name text not null,
	category text not null,
	knownby text not null,
	tableno text not null,
	memo text
);