truncate table alembic_version;
create schema if not exists core;

create sequence if not exists core.profile_seq start 1;
create sequence if not exists core.settlement_seq start 1;
create sequence if not exists core.user_seq start 1;
create sequence if not exists core.device_session_seq start 1;
create sequence if not exists core.profile_interests_seq start 1;
create sequence if not exists core.interest_seq start 1;
create sequence if not exists core.profile_photo_seq start 1;


INSERT INTO core.interest (name)
VALUES ('Путешествия'), ('Кино'), ('Фитнес'), ('Готовка'), ('Музыка'),
       ('Фотография'), ('Искусство'), ('Чтение'), ('Автомобили'), ('Технологии'),
       ('Культура'), ('Спорт'), ('Рестораны'), ('Домашние животные'), ('Бег');
commit




