
BEGIN TRANSACTION;

drop table if exists scraped_inventory_data.inventories_backup;

-- auto-generated definition
create table scraped_inventory_data.inventories_backup
(
    vin                varchar not null,
    title              varchar,
    year               integer,
    make               varchar,
    model              varchar,
    trim               varchar,
    model_trim         varchar,
    price              money,
    mileage            integer,
    vehicle_type       varchar,
    interior_color     varchar,
    exterior_color     varchar,
    transmission       varchar,
    engine             varchar,
    drivetrain         varchar,
    dealership_name    varchar,
    dealership_address varchar,
    dealership_zipcode varchar,
    dealership_city    varchar,
    dealership_state   varchar,
    scraped_url        varchar,
    scraped_date       timestamp,
    scraped_month      date,
    CONSTRAINT inventories_pk_backup PRIMARY KEY (vin, scraped_month)
);

insert into scraped_inventory_data.inventories_backup select * from scraped_inventory_data.inventories;

COMMIT;
