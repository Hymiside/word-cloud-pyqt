create table patterns (
    id integer primary key,
    title text not null,
    word_cloud text not null,
    user_id integer not null references users(id)
);

create table users (
    id integer primary key,
    login text not null,
    hash text not null,
    salt text not null,
    phone text not null
);