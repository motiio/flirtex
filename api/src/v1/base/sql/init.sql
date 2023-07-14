CREATE OR REPLACE FUNCTION set_displaying_order()
    RETURNS TRIGGER AS
$BODY$
declare
    photo_count integer;
BEGIN
    select count(1) into photo_count from core.photo where profile_id = NEW.profile_id;

    IF NEW.displaying_order IS NULL THEN
        NEW.displaying_order := photo_count + 1;
    END IF;

    RETURN NEW;
END;
$BODY$
    LANGUAGE plpgsql;

CREATE TRIGGER set_displaying_order_trigger
    BEFORE INSERT
    ON core.photo
    FOR EACH ROW
EXECUTE FUNCTION set_displaying_order();


CREATE
    OR REPLACE FUNCTION update_displaying_order()
    RETURNS TRIGGER AS
$BODY$
declare
    min_displaying_order INTEGER := 1;
    max_displaying_order
                         INTEGER;
BEGIN
    SELECT count(displaying_order)
    INTO max_displaying_order
    FROM core.photo
    WHERE profile_id = NEW.profile_id;

    IF NEW.displaying_order <> OLD.displaying_order THEN
        IF NEW.displaying_order < OLD.displaying_order THEN
            -- Decrement displaying_order for the photos between NEW and OLD positions
            UPDATE core.photo
            SET displaying_order = displaying_order + 1
            WHERE profile_id = NEW.profile_id
              AND displaying_order >= NEW.displaying_order
              AND displaying_order < OLD.displaying_order
              AND id <> NEW.id;
        ELSE
            UPDATE core.photo
            SET displaying_order = displaying_order - 1
            WHERE profile_id = NEW.profile_id
              AND displaying_order > OLD.displaying_order
              AND displaying_order <= NEW.displaying_order
              AND id <> NEW.id;
        END IF;
        UPDATE core.photo
        SET displaying_order = case
                                   when NEW.displaying_order > max_displaying_order then max_displaying_order
                                   when NEW.displaying_order < min_displaying_order then min_displaying_order
                                   else NEW.displaying_order end
        WHERE profile_id = NEW.profile_id
          AND id = NEW.id;
    END IF;

    RETURN NEW;
END;
$BODY$
    LANGUAGE plpgsql;

CREATE TRIGGER update_displaying_order_trigger
    after UPDATE OF displaying_order
    ON core.photo
    FOR EACH ROW
EXECUTE FUNCTION update_displaying_order();


insert into core.interest (id, name, icon, created_at, updated_at)
values (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring), 'Путешествия', 'svg',
        current_timestamp, current_timestamp),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring), 'Кино', 'svg',
        current_timestamp, current_timestamp),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring), 'Фитнес', 'svg',
        current_timestamp, current_timestamp),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring), 'Готовка', 'svg',
        current_timestamp, current_timestamp),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring), 'Музыка', 'svg',
        current_timestamp, current_timestamp),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring), 'Фотография', 'svg',
        current_timestamp, current_timestamp),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring), 'Искусство', 'svg',
        current_timestamp, current_timestamp),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring), 'Чтение', 'svg',
        current_timestamp, current_timestamp),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring), 'Автомобили', 'svg',
        current_timestamp, current_timestamp),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring), 'Технологии', 'svg',
        current_timestamp, current_timestamp),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring), 'Культура', 'svg',
        current_timestamp, current_timestamp),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring), 'Спорт', 'svg',
        current_timestamp, current_timestamp),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring), 'Рестораны', 'svg',
        current_timestamp, current_timestamp),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring), 'Домашние животные',
        'svg', current_timestamp, current_timestamp),
       (uuid_in(overlay(overlay(md5(random()::text || ':' || random()::text) placing '4' from 13) placing
                        to_hex(floor(random() * (11 - 8 + 1) + 8)::int)::text from 17)::cstring), 'Бег', 'svg',
        current_timestamp, current_timestamp);

commit;

drop table if exists core.like;
drop table if exists core.skip;
drop table if exists core.match;
drop table if exists core.save;

create table core.like
(
    source_profile uuid      not null
        references core.profile
            on delete cascade,
    target_profile uuid      not null
        references core.profile
            on delete cascade,
    created_at     timestamp not null,
    updated_at     timestamp not null
) partition by list (source_profile);
CREATE INDEX IF NOT EXISTS idx_like_source_profile ON core.like (source_profile);
CREATE INDEX IF NOT EXISTS idx_like_target_profile ON core.like (target_profile);

create table core.skip
(
    source_profile uuid      not null
        references core.profile
            on delete cascade,
    target_profile uuid      not null
        references core.profile
            on delete cascade,
    created_at     timestamp not null,
    updated_at     timestamp not null
) partition by list (source_profile);
CREATE INDEX IF NOT EXISTS idx_skip_source_profile ON core.skip (source_profile);
CREATE INDEX IF NOT EXISTS idx_skip_target_profile ON core.skip (target_profile);

create table core.match
(
    profile_1  uuid      not null
        references core.profile
            on delete cascade,
    profile_2  uuid      not null
        references core.profile
            on delete cascade,
    created_at timestamp not null,
    updated_at timestamp not null
);
CREATE INDEX IF NOT EXISTS idx_skip_profile_1 ON core.match (profile_1);
CREATE INDEX IF NOT EXISTS idx_skip_profile_2 ON core.match (profile_2);

create table core.save
(
    profile_id       uuid      not null
        references core.profile
            on delete cascade,
    saved_profile_id uuid      not null
        references core.profile
            on delete cascade,
    created_at       timestamp not null,
    updated_at       timestamp not null
)partition by list (profile_id);
CREATE INDEX IF NOT EXISTS idx_skip_profile_1 ON core.save (profile_id);
CREATE INDEX IF NOT EXISTS idx_skip_profile_2 ON core.save (saved_profile_id);




