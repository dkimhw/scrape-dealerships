alter table scraped_inventory_data.inventories add column scraped_month date;
select scraped_date, scraped_month from scraped_inventory_data.inventories LIMIT 100;

UPDATE scraped_inventory_data.inventories
SET scraped_month = date_trunc('month', scraped_date);


alter table scraped_inventory_data.inventories alter column scraped_month set not null;

ALTER TABLE scraped_inventory_data.inventories
  ADD CONSTRAINT inventories_pk
    PRIMARY KEY (vin, scraped_month);
