CREATE DATABASE shard;

CREATE TABLE shard.users_activities (
    id UUID,
    user_id UUID,
    film_id UUID,
    event_name String,
    comment Nullable(String),
    film_sec Nullable(Int64),
    like Nullable(Bool),
    event_time DateTime
) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/users_activities', 'replica_1') PARTITION BY toYYYYMMDD(event_time) ORDER BY id;

CREATE TABLE default.users_activities (
    id UUID,
    user_id UUID,
    film_id UUID,
    event_name String,
    comment Nullable(String),
    film_sec Nullable(Int64),
    like Nullable(Bool),
    event_time DateTime
) ENGINE = Distributed('company_cluster', '', users_activities, rand());
