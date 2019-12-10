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

USE `Charity`;

-- -----------------------------------------------------
-- Table `mydb`.`Recipients`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Charity`.`Recipients` (
  `RE_NUM` INT NOT NULL,
  `RE_NAME` VARCHAR(45) NULL,
  `RE_ADDRESS` VARCHAR(45) NULL,
  `RE_CITY` VARCHAR(45) NULL,
  `RE_STATE` VARCHAR(45) NULL,
  `RE_ZIP` VARCHAR(45) NULL,
  `RE_EMAIL` VARCHAR(45) NULL,
  `RE_PHONE` VARCHAR(45) NULL,
  PRIMARY KEY (`RE_NUM`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
