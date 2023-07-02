truncate table alembic_version;
drop schema core cascade ;
create schema if not exists core;

create sequence if not exists core.profile_seq start 1;
create sequence if not exists core.settlement_seq start 1;
create sequence if not exists core.user_seq start 1;
create sequence if not exists core.device_session_seq start 1;
create sequence if not exists core.profile_interests_seq start 1;
create sequence if not exists core.interest_seq start 1;
create sequence if not exists core.profile_photo_seq start 1;
select *
from core.profile_interests;
select * from core.profile;
select * from core.interest;
select * from core.profile_interests;
truncate core.profile cascade ;

SELECT uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                       to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring);



INSERT INTO core.interest (id, name, created_at, updated_at, icon)
VALUES (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring),
        'Путешествия',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP,
        'svg'
        ),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring),
        'Кино',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP,
        'svg'),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring),
        'Фитнес',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP,
        'svg'),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring),
        'Готовка',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP,
        'svg'),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring),
        'Музыка',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP,
        'svg'),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring),
        'Фотография',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP,
        'svg'),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring),
        'Искусство',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP,
        'svg'),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring),
        'Чтение',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP,
        'svg'),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring),
        'Автомобили',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP,
        'svg'),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring),
        'Технологии',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP,
        'svg'),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring),
        'Культура',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP,
        'svg'),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring),
        'Спорт',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP,
        'svg'),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring),
        'Рестораны',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP,
        'svg'),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring),
        'Домашние животные',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP,
        'svg'),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring),
        'Бег',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP,
        'svg');
commit



truncate table alembic_version;

