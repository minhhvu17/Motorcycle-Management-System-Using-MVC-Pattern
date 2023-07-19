use `motorbikemanagement`;

drop table if exists product;
drop table if exists category;
drop table if exists brand;
drop table if exists orders;

CREATE TABLE IF NOT EXISTS Brand (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) CHARACTER SET utf8,
  `quantity` INT DEFAULT 0,
  INDEX brand_idx(name),
  CONSTRAINT `quantity_brand` CHECK (`quantity` >= 0)
);

INSERT INTO Brand(name) VALUES 
  ('Honda'),
  ('Yamaha'),
  ('Ducati'),
  ('Suzuki');


CREATE TABLE IF NOT EXISTS Category(
	`id` int AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) CHARACTER SET utf8,
    `quantity` INT DEFAULT 0,
    INDEX cate_idx(name),
    CONSTRAINT `quantity_category` CHECK (`quantity` >= 0)
);

INSERT INTO Category(name) VALUES 
  ('manual'),
  ('scooter'),
  ('sport');

CREATE TABLE IF NOT EXISTS product (
    `ID` INT primary key auto_increment,
    `Name` VARCHAR(33) CHARACTER SET utf8,
    `Brand` VARCHAR(6) CHARACTER SET utf8,
    `Category` VARCHAR(7) CHARACTER SET utf8,
    `Length_mm` INT,
    `Width_mm` INT,
    `Height_mm` INT,
    `Mass_kg` INT,
    `Fuel_Capacity_l` NUMERIC(3, 1),
    `Fuel_Consumption_l_100km` NUMERIC(3, 2),
    `Engine_Type` VARCHAR(22) CHARACTER SET utf8,
    `Maximize_Efficiency_kW_minute` NUMERIC(5, 2),
    `Color` VARCHAR(18) CHARACTER SET utf8,
    `Selling_Price_M` NUMERIC(15, 3),
    `quanity` INT,
    CONSTRAINT `quanity` CHECK (`quanity` >= 0)
);
DROP TRIGGER IF EXISTS update_brand_quantity;
DELIMITER $$
CREATE TRIGGER update_brand_quantity AFTER INSERT ON Product
FOR EACH ROW
BEGIN
    UPDATE Brand
    SET quantity = quantity + new.quanity
    WHERE name = new.Brand;
    
    UPDATE Category
    SET quantity = quantity + new.quanity
    WHERE name = new.Category;
END $$
DELIMITER ;


INSERT INTO product (name, brand, category, length_mm, width_mm, height_mm, mass_kg, fuel_capacity_l, fuel_consumption_l_100km, engine_type, Maximize_Efficiency_kW_minute, color, Selling_Price_M, quanity) 
Values	
	('HEHEHEHEHEH','Yamaha','Scooter',2128,749,1149,207,15,5.17,'4-stroke',61.7,'red, black',254.5,0),
	('CBR650R Version 2023','Yamaha','Scooter',2128,749,1149,207,15,5.17,'4-stroke',61.7,'red, black',254.5,8),
	('CBR650 Version 2023','Yamaha','Sport',2128,784,1076,202,15,4.99,'4-stroke',61.7,'black',246.5,12),
	('SH Mode 125cc','Honda','Manual',1950,669,1100,116,5.6,2.16,'4-stroke',8.2,'blue, black',62.8,20),
	('Africa Twin 2023 Adventure Sports','Yamaha','Scooter',2330,960,1545,250,24.8,4.9,'4-stroke',75,'white, blue, black',720.5,9),
	('Africa Twin 2023 Standard','Yamaha','Manual',2330,960,1395,229,18.8,4.9,'4-stroke',75,'black',590.5,8),
	('Rebel 500','Suzuki','Scooter',2206,822,1093,190,11.2,3.42,'DOHC, 4-stroke',33.5,'red, black',180.8,14),
	('CB1000R','Honda','Scooter',2120,789,1090,213,16.2,5.95,'4-stroke',107,'black',525,1),
	('Future 125 FI','Honda','Manual',1931,711,1083,105,4.6,1.54,'4-stroke',6.83,'white, black',32.1,6),
	('Vision','Honda','Manual',1871,686,1101,95,4.9,1.85,'4-stroke',6.59,'white, black',31.3,3),
	('Vario 160','Suzuki','Sport',1929,678,1088,117,5.5,2.2,'4-stroke',11.3,'blue, black, grey',52.2,4),
	('SH160i','Honda','Manual',2090,739,1129,133,7.8,2.24,'PGM-FI, 4-stroke',12.4,'white, black',82.8,5),
	('SH125i','Honda','Scooter',2090,739,1129,133,7.8,2.46,'PGM-FI, 4-stroke',9.6,'white, black',82.8,3),
	('Wave RSX FI 110','Ducati','Manual',1921,709,1081,99,4,1.7,'4-stroke',6.46,'red, black',22.1,15),
	('Wave Alpha 110cc','Ducati','Scooter',1914,688,1075,97,3.7,1.9,'4-stroke',6.12,'black',18.8,5),
	('Winner X','Honda','Scooter',2019,727,1104,122,4.5,1.99,'PGM-FI, 4-stroke',11.5,'black, yellow',46.2,3),
	('CBR500R','Suzuki','Scooter',2080,760,1145,192,17.1,3.59,'4-stroke',35,'black',192.5,11),
	('CB500X','Suzuki','Manual',2155,830,1410,199,17.5,3.59,'4-stroke',35,'black',193.8,6),
	('CB500F','Suzuki','Manual',2080,800,1060,189,17.1,3.59,'4-stroke',35,'black',184.5,17),
	('CB150R The Streetster','Suzuki','Manual',1973,822,1053,126,8.5,2.79,'4-stroke',12,'black',105.5,10),
	('Air Blade 125','Honda','Manual',1887,687,1092,113,4.4,2.26,'4-stroke',8.75,'black, yellow',43.3,17),
	('Air Blade 160','Yamaha','Sport',1890,686,1116,114,4.4,2.3,'4-stroke',11.2,'black, yellow',43.3,1),
	('Gold Wing 2022','Ducati','Sport',2615,905,1555,390,21,5.53,'4-stroke',93,'black',1231,15),
	('Rebel 1100 2022 DCT','Honda','Manual',2240,834,1115,233,13.6,5.3,'4-stroke',64,'black',499,13),
	('Rebel 1100 2022','Honda','Manual',2240,853,1115,223,13.6,5.3,'4-stroke',64,'black',449,2),
	('Blade 110','Ducati','Sport',1920,702,1075,98,3.7,1.85,'4-stroke',6.18,'black, red',21.7,18),
	('Lead 125cc','Honda','Manual',1844,680,1130,113,6,2.16,'4-stroke',8.22,'white',39.8,19),
	('Super Cub C125','Honda','Scooter',1910,718,1002,109,3.7,1.5,'PGM-FI, 4-stroke',6.87,'blue, white',87.4,16),
	('CBR150R','Yamaha','Scooter',1983,700,1090,139,12,2.91,'PGM-FI, DOHC, 4-stroke',12.6,'black, red',71.3,7),
	('CBR1000RR-R Fireblade SP','Yamaha','Sport',2100,745,1140,201,16.1,6.3,'PGM-FI, DOHC, 4-stroke',160,'red, blue, white',1050,18),
	('CBR1000RR-R Fireblade','Yamaha','Sport',2100,745,1140,201,16.1,6.3,'PGM-FI, DOHC, 4-stroke',160,'black',950,12);
    
CREATE TABLE IF NOT EXISTS orders (
                ID INT primary key auto_increment,
                Date DATETIME,
                Customer_Name VARCHAR(255) CHARACTER SET utf8,
                Customer_Phone VARCHAR(255) CHARACTER SET utf8,
                Model VARCHAR(255) CHARACTER SET utf8,
                Brand VARCHAR(255) CHARACTER SET utf8,
                Category VARCHAR(255) CHARACTER SET utf8,
                Color VARCHAR(255) CHARACTER SET utf8,
                Quantity INT default 1,
                price NUMERIC(18, 3)
);

select * from product;
select * from brand;
select * from category;
select * from orders;