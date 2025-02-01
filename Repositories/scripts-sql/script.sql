DROP TABLE Portfolio;
DROP TABLE Person;
DROP TABLE Image;
DROP TABLE Authentication;

CREATE TABLE Person (
    PersonId int AUTO_INCREMENT PRIMARY KEY,
    PersonName VARCHAR(1000) NULL,
    Cpf VARCHAR(50) NULL,
    Phone VARCHAR(50) NULL,
    Mail VARCHAR(100) NULL,
    RegisterDate TIMESTAMP NULL,
    HasAcceptedParticipation BOOLEAN,
    ExternalCode varchar(1000) NULL,
    BalanceCurrentValue int
);

CREATE TABLE Balance (
    BalanceId int AUTO_INCREMENT PRIMARY KEY,
    Impact int,
    BalanceCurrentValue int,
    Operation int NOT NULL,
    ImpactDate TIMESTAMP NOT NULL,
    ImpactOrigin int NOT NULL,
    PersonId int NULL,
    OrganizerId int NULL,
    EventDayId int NOT NULL,
    FOREIGN KEY (PersonId) REFERENCES Person(PersonId),
    FOREIGN KEY (OrganizerId) REFERENCES Organizer(OrganizerId),
    FOREIGN KEY (EventDayId) REFERENCES Calendar(EventDayId)
);

CREATE TABLE Organizer (
    OrganizerId int AUTO_INCREMENT PRIMARY KEY,
    OrganizerName VARCHAR(1000),
    Login VARCHAR(50) UNIQUE,
    SecretKey VARCHAR(50)
);

CREATE TABLE Calendar (
    EventDayId int PRIMARY KEY NOT NULL,
    InitialDatetime DATETIME NOT NULL,
    FinalDatetime DATETIME NOT NULL
);

CREATE TABLE Gift (
    GiftId int PRIMARY KEY NOT NULL,
    GiftName VARCHAR(1000) NOT NULL,
);

CREATE TABLE Award (
    AwardId int AUTO_INCREMENT PRIMARY KEY,
    OrganizerId int NOT NULL,
    GiftId int NOT NULL,
    PersonId int,
    AwardStatus int NOT NULL,
    PredefinedDateTime DATETIME NOT NULL,
    AwardDate DATETIME,
    EventDayId int NOT NULL,
    IsUpdated BINARY,
    FOREIGN KEY (OrganizerId) REFERENCES Organizer(OrganizerId),
    FOREIGN KEY (GiftId) REFERENCES Gift(GiftId),
    FOREIGN KEY (PersonId) REFERENCES Person(PersonId),
    FOREIGN KEY (EventDayId) REFERENCES Calendar(EventDayId)
);

CREATE TABLE Image (
    ImageId int AUTO_INCREMENT PRIMARY KEY,
    ImageName VARCHAR(100),
    IsDownloaded BOOLEAN not null,
    PersonId int,
    RegisterDate TIMESTAMP NULL,
    FOREIGN KEY (PersonId) REFERENCES Person(PersonId)
);