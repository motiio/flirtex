drop function if exists core.deck;

create or replace function core.deck(p_profile_id uuid)
    RETURNS TABLE
            (
                profile_id uuid
            )
AS
$$
BEGIN
    RETURN QUERY
        with all_profiles as (select p.id, p.gender, f.looking_gender, p.location, p.birthdate
                              from core.profile p
                                       join core.filter f on p.id = f.profile_id),
             me as (select p.id, p.gender, f.looking_gender, p.location, f.max_distance, f.age_from, f.age_to
                    from core.profile p
                             join core.filter f on p.id = f.profile_id
                    where p.id = p_profile_id)
        select all_profiles.id
        from all_profiles
                 join me on case
                                when me.looking_gender::text != 'nevermind' then
                                    case
                                        when me.looking_gender::text = all_profiles.gender::text
                                            and (all_profiles.looking_gender::text = me.gender::text
                                                or all_profiles.looking_gender::text = 'nevermind') then true
                                        else false
                                        end
                                else
                                    case
                                        when all_profiles.looking_gender::text = me.gender::text
                                            or all_profiles.looking_gender::text = 'nevermind' then true
                                        else false
                                        end
            end
                 left
                     join core.like l
                          on l.source_profile = me.id
                              and l.target_profile = all_profiles.id
                 left
                     join core.skip s
                          on s.source_profile = me.id
                              and s.target_profile = all_profiles.id
        where all_profiles.id != me.id
          and l.id is null
          and s.id is null
          and ST_DWithin(
                all_profiles.location::geography,
                me.location::geography,
                me.max_distance * 1000-- расстояние в метрах (1 км = 1000 м)
            )
        and extract(year from age(current_date, all_profiles.birthdate)) between me.age_from and me.age_to;
END ;
$$ LANGUAGE plpgsql;
