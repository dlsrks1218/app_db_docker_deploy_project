-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Salesperson`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Salesperson` (
  `s_no` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`s_no`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Customer` (
  `c_no` INT NOT NULL AUTO_INCREMENT,
  `ticket_cnt` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `age` INT NULL,
  `address` VARCHAR(45) NULL,
  `phone` VARCHAR(45) NULL,
  `id_no` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`c_no`, `ticket_cnt`),
  UNIQUE INDEX `id_no_UNIQUE` (`id_no` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Car`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Car` (
  `car_no` INT NOT NULL AUTO_INCREMENT,
  `s_no` INT NULL DEFAULT NULL,
  `c_no` INT NULL DEFAULT NULL,
  `brand` VARCHAR(45) NULL,
  `year` YEAR(4) NULL,
  `model` VARCHAR(45) NULL,
  `color` VARCHAR(45) NULL,
  PRIMARY KEY (`car_no`),
  INDEX `fk_Car_Salesperson1_idx` (`s_no` ASC),
  INDEX `fk_Car_Customer1_idx` (`c_no` ASC),
  CONSTRAINT `fk_Car_Salesperson1`
    FOREIGN KEY (`s_no`)
    REFERENCES `mydb`.`Salesperson` (`s_no`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Car_Customer1`
    FOREIGN KEY (`c_no`)
    REFERENCES `mydb`.`Customer` (`c_no`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Invoice`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Invoice` (
  `invoice_no` INT NOT NULL AUTO_INCREMENT,
  `s_no` INT NOT NULL,
  `c_no` INT NOT NULL,
  PRIMARY KEY (`invoice_no`),
  INDEX `fk_Invoice_Salesperson1_idx` (`s_no` ASC),
  INDEX `fk_Invoice_Customer1_idx` (`c_no` ASC),
  CONSTRAINT `fk_Invoice_Salesperson1`
    FOREIGN KEY (`s_no`)
    REFERENCES `mydb`.`Salesperson` (`s_no`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Invoice_Customer1`
    FOREIGN KEY (`c_no`)
    REFERENCES `mydb`.`Customer` (`c_no`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Parts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Parts` (
  `p_no` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `p_cnt` INT NULL DEFAULT 30,
  PRIMARY KEY (`p_no`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Repair-or-Service`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Repair-or-Service` (
  `service_no` INT NOT NULL AUTO_INCREMENT,
  `history` VARCHAR(45) NOT NULL,
  `c_no` INT NOT NULL,
  `p_no` INT NOT NULL,
  PRIMARY KEY (`service_no`),
  INDEX `fk_Repair-or-Service_Customer1_idx` (`c_no` ASC),
  INDEX `fk_Repair-or-Service_Parts1_idx` (`p_no` ASC),
  CONSTRAINT `fk_Repair-or-Service_Customer1`
    FOREIGN KEY (`c_no`)
    REFERENCES `mydb`.`Customer` (`c_no`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Repair-or-Service_Parts1`
    FOREIGN KEY (`p_no`)
    REFERENCES `mydb`.`Parts` (`p_no`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Mechanic`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Mechanic` (
  `m_no` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`m_no`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Work`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Work` (
  `service_no` INT NOT NULL,
  `m_no` INT NOT NULL,
  `work_date` DATE NOT NULL,
  PRIMARY KEY (`service_no`, `m_no`),
  INDEX `fk_Repair-or-Service_has_Mechanic_Mechanic1_idx` (`m_no` ASC),
  INDEX `fk_Repair-or-Service_has_Mechanic_Repair-or-Service1_idx` (`service_no` ASC),
  CONSTRAINT `fk_Repair-or-Service_has_Mechanic_Repair-or-Service1`
    FOREIGN KEY (`service_no`)
    REFERENCES `mydb`.`Repair-or-Service` (`service_no`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Repair-or-Service_has_Mechanic_Mechanic1`
    FOREIGN KEY (`m_no`)
    REFERENCES `mydb`.`Mechanic` (`m_no`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Account`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Account` (
  `ac_no` INT NOT NULL AUTO_INCREMENT,
  `id` VARCHAR(20) NOT NULL,
  `pw` VARCHAR(20) NOT NULL,
  `s_no` INT NULL,
  `c_no` INT NULL,
  PRIMARY KEY (`ac_no`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  INDEX `fk_Account_Salesperson1_idx` (`s_no` ASC),
  INDEX `fk_Account_Customer1_idx` (`c_no` ASC),
  CONSTRAINT `fk_Account_Salesperson1`
    FOREIGN KEY (`s_no`)
    REFERENCES `mydb`.`Salesperson` (`s_no`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Account_Customer1`
    FOREIGN KEY (`c_no`)
    REFERENCES `mydb`.`Customer` (`c_no`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- ALTER TABLE Customer CONVERT TO character SET utf8;
-- ALTER TABLE Salesperson CONVERT TO character SET utf8;
-- ALTER TABLE Account CONVERT TO character SET utf8;
-- ALTER TABLE Mechanic CONVERT TO character SET utf8;
-- ALTER TABLE Parts CONVERT TO character SET utf8;
-- ALTER TABLE `Repair-or-Service` CONVERT TO character SET utf8;
-- ALTER TABLE Work TO character SET utf8;
-- ALTER TABLE Car CONVERT TO character SET utf8;

insert into Customer(ticket_cnt, name, age, address, phone, id_no) values(0, "임종현", 28, "서울시 서대문구", "010-1234-1234", "930000-1234567");
insert into Customer(ticket_cnt, name, age, address, phone, id_no) values(0, "설준명", 29, "서울시 용산구", "010-1234-9876", "930000-3456789");
insert into Customer(ticket_cnt, name, age, address, phone, id_no) values(0, "이승준", 28, "서울시 중랑구", "010-3456-5678", "920000-1234567");

INSERT INTO Salesperson(NAME) VALUES('Bob');
INSERT INTO Salesperson(NAME) VALUES('Constantine');
INSERT INTO Salesperson(NAME) VALUES('Dembele');

INSERT INTO Account(id, pw, s_no) VALUES('manager1', 'manager', 1);
INSERT INTO Account(id, pw, s_no) VALUES('manager2', 'manager', 2);
INSERT INTO Account(id, pw, s_no) VALUES('manager3', 'manager', 3);
INSERT INTO Account(id, pw, c_no) VALUES('user1', 'user', 1);
INSERT INTO Account(id, pw, c_no) VALUES('user2', 'user', 2);
INSERT INTO Account(id, pw, c_no) VALUES('user3', 'user', 3);

INSERT INTO Mechanic(name) VALUES('Han Byul');
INSERT INTO Mechanic(name) VALUES('Jin Woo');
INSERT INTO Mechanic(name) VALUES('Do Won');

INSERT INTO Parts(name) VALUES('Handle');
INSERT INTO Parts(name) VALUES('Wheel');
INSERT INTO Parts(name) VALUES('Door');

INSERT INTO `Repair-or-Service`(history, c_no, p_no) VALUES('1/Handle/2020-07-08', 1, 3);
INSERT INTO `Repair-or-Service`(history, c_no, p_no) VALUES('2/Wheel/2020-07-12', 2, 2);
INSERT INTO `Repair-or-Service`(history, c_no, p_no) VALUES('3/Handle/2020-07-15', 3, 1);
INSERT INTO `Repair-or-Service`(history, c_no, p_no) VALUES('1/Door/2020-07-13', 1, 3);
INSERT INTO `Repair-or-Service`(history, c_no, p_no) VALUES('2/Door/2020-07-21', 2, 3);
INSERT INTO `Repair-or-Service`(history, c_no, p_no) VALUES('3/Handle/2020-07-27', 3, 1);
INSERT INTO `Repair-or-Service`(history, c_no, p_no) VALUES('1/Door/2020-07-10', 1, 1);
INSERT INTO `Repair-or-Service`(history, c_no, p_no) VALUES('2/Door/2020-07-14', 2, 3);
INSERT INTO `Repair-or-Service`(history, c_no, p_no) VALUES('3/Wheel/2020-07-24', 3, 2);

INSERT INTO Work(service_no, m_no, work_date) VALUES(1, 1,'2020-07-08');
INSERT INTO Work(service_no, m_no, work_date) VALUES(2, 1,'2020-07-12');
INSERT INTO Work(service_no, m_no, work_date) VALUES(3, 1,'2020-07-15');
INSERT INTO Work(service_no, m_no, work_date) VALUES(4, 2,'2020-07-13');
INSERT INTO Work(service_no, m_no, work_date) VALUES(5, 2,'2020-07-21');
INSERT INTO Work(service_no, m_no, work_date) VALUES(6, 2,'2020-07-27');
INSERT INTO Work(service_no, m_no, work_date) VALUES(7, 3,'2020-07-10');
INSERT INTO Work(service_no, m_no, work_date) VALUES(8, 3,'2020-07-14');
INSERT INTO Work(service_no, m_no, work_date) VALUES(9, 3,'2020-07-24');

INSERT INTO Car(s_no, c_no, brand, year, model, color) values (1, NULL,'BMW', '2019', 'm6', 'black');
INSERT INTO Car(s_no, c_no, brand, year, model, color) VALUES (2, NULL,'Volvo', '2017', 'xc90', 'silver');
INSERT INTO Car(s_no, c_no, brand, year, model, color) VALUES (3, NULL, 'Kia', '2020', 'k5', 'blue');
INSERT INTO Car(s_no, c_no, brand, year, model, color) VALUES (NULL, 1,'Hyundai', '2018', 'Sonata', 'gray');
INSERT INTO Car(s_no, c_no,brand, year, model, color) VALUES (NULL, 2,'SSangyong', '2011', 'Musso', 'white');
INSERT INTO Car(s_no, c_no,brand, year, model, color) VALUES (NULL, 3,'Hyundai', '2012', 'Grandeur', 'black');

