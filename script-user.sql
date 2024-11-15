drop table if exists Services_List;
drop table if exists Services_Approbation_List;
drop table if exists Users;
drop table if exists Services;

-- Create table for Users
CREATE TABLE IF NOT EXISTS Users
(
    UID      INT PRIMARY KEY AUTO_INCREMENT,
    UserName VARCHAR(255)   NOT NULL,
    Password VARBINARY(255) NOT NULL, -- Storing password as hash
    Name     VARCHAR(255),
    Role     INT NOT NULL DEFAULT 0,
    IsConnected BOOLEAN NOT NULL DEFAULT FALSE
);

-- Create table for Services
CREATE TABLE IF NOT EXISTS Services
(
    SID  INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Link VARCHAR(255),
    Approbation INT NOT NULL DEFAULT 0,
    Description TEXT
);

-- Create table for Services_List
CREATE TABLE IF NOT EXISTS Services_List
(
    ID  INT PRIMARY KEY AUTO_INCREMENT,
    UID INT NOT NULL,
    SID INT NOT NULL,
    ReceiveDate DATE NOT NULL,
    FOREIGN KEY (UID) REFERENCES Users (UID) ON DELETE CASCADE,
    FOREIGN KEY (SID) REFERENCES Services (SID) ON DELETE CASCADE
);

-- Create table for Services_Approbation_List
CREATE TABLE IF NOT EXISTS Services_Approbation_List
(
    ID  INT PRIMARY KEY AUTO_INCREMENT,
    UID INT NOT NULL,
    SID INT NOT NULL,
    ClaimDate DATE NOT NULL,
    FOREIGN KEY (UID) REFERENCES Users (UID) ON DELETE CASCADE,
    FOREIGN KEY (SID) REFERENCES Services (SID) ON DELETE CASCADE
);

# create a user
INSERT INTO Users (UserName, Password, Name, Role) VALUES ('alberic@alberic-wds.fr', 'owner', 'Owner', 2);