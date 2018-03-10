drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username text not null,
  password blob not null,
  created text not null,
  admin integer not null
);
