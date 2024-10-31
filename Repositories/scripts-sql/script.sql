CREATE TABLE Person (
    PersonId int AUTO_INCREMENT PRIMARY KEY,
    PersonName VARCHAR(1000) NULL,
    Cpf VARCHAR(50) NULL,
    Phone VARCHAR(50) NULL,
    BirthDate DATETIME NULL,
    Mail VARCHAR(100) NULL,
    RegisterDate TIMESTAMP NULL,
    HasAcceptedPromotion BINARY,
    HasAcceptedParticipation BINARY,
);

CREATE TABLE Image (
    ImageId VARCHAR(100) PRIMARY KEY,
    ImageName VARCHAR(800),
    RegisterDate TIMESTAMP NULL,
    Active BINARY,
    IsDeleted BINARY
);

CREATE TABLE Portfolio (
	PortfolioId int AUTO_INCREMENT PRIMARY KEY,
	ImageId varchar(100),
    PersonId int,
    FOREIGN KEY (PersonId) REFERENCES Person(PersonId),
    FOREIGN KEY (ImageId) REFERENCES Image(ImageId)
);


