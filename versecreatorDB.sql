-- ------------------------------------------------------------
-- An entity can be a place, object, thing, concept whatever.
-- ------------------------------------------------------------

CREATE TABLE tblEntity (
  ID INTEGER  NOT NULL  ,
  Text TEXT    ,
  EntityType VARCHAR(255)      ,
PRIMARY KEY(ID));



CREATE TABLE tblCharacter (
  ID INTEGER  NOT NULL  ,
  Name INTEGER    ,
  Description INTEGER    ,
  PersonalityDesc INTEGER    ,
  Gender VARCHAR(255)    ,
  CreatedDateTime DATETIME      ,
PRIMARY KEY(ID));



-- ------------------------------------------------------------
-- Table that holds user information.
-- ------------------------------------------------------------

CREATE TABLE tblUser (
  ID INTEGER  NOT NULL  ,
  UserName VARCHAR(255)    ,
  FirstName VARCHAR(255)    ,
  LastName VARCHAR(255)    ,
  Pass VARCHAR(255)    ,
  Bio TEXT      ,
PRIMARY KEY(ID));



-- ------------------------------------------------------------
-- Stores groups available within the Verse application
-- ------------------------------------------------------------

CREATE TABLE tblGroup (
  ID INTEGER  NOT NULL  ,
  Name VARCHAR(255)    ,
  Description TEXT      ,
PRIMARY KEY(ID));



CREATE TABLE tblChapter (
  ID INTEGER  NOT NULL  ,
  Name VARCHAR(255)    ,
  WrdLength INTEGER    ,
  Text LONGTEXT    ,
  CreatedDateTime DATETIME      ,
PRIMARY KEY(ID));



CREATE TABLE infEntityTypes (
  ID INTEGER  NOT NULL  ,
  Name VARCHAR(255)    ,
  Description TEXT      ,
PRIMARY KEY(ID));



CREATE TABLE infAttributes (
  ID INTEGER  NOT NULL  ,
  Name INTEGER    ,
  Description INTEGER      ,
PRIMARY KEY(ID));



CREATE TABLE infCharacterRole (
  Role INTEGER  NOT NULL  ,
  ID INTEGER    ,
  Name INTEGER    ,
  Description INTEGER      ,
PRIMARY KEY(Role));



CREATE TABLE infRelationTypes (
  ID INTEGER  NOT NULL  ,
  Name VARCHAR(255)    ,
  Description TEXT      ,
PRIMARY KEY(ID));



CREATE TABLE tblConfigPermissions (
  PermID INTEGER  NOT NULL  ,
  GroupID INTEGER  NOT NULL    ,
PRIMARY KEY(PermID),
  FOREIGN KEY(GroupID)
    REFERENCES tblGroup(ID)
      ON DELETE CASCADE
      ON UPDATE CASCADE);



-- ------------------------------------------------------------
-- This table holds meta information about a Fictional Universe (or 'verse')
-- ------------------------------------------------------------

CREATE TABLE tblVerseMetaInfo (
  ID INTEGER  NOT NULL  ,
  UserID INTEGER  NOT NULL  ,
  Name VARCHAR(255)    ,
  Description TEXT    ,
  Creator VARCHAR(255)      ,
PRIMARY KEY(ID),
  FOREIGN KEY(UserID)
    REFERENCES tblUser(ID)
      ON DELETE SET NULL
      ON UPDATE SET NULL);



CREATE TABLE tblCharacterAttributes (
  ID INTEGER  NOT NULL  ,
  CharacterID INTEGER  NOT NULL  ,
  Name VARCHAR(255)    ,
  Value VARCHAR(255)      ,
PRIMARY KEY(ID),
  FOREIGN KEY(CharacterID)
    REFERENCES tblCharacter(ID)
      ON DELETE CASCADE
      ON UPDATE CASCADE);



-- ------------------------------------------------------------
-- Contains user memberships to groups
-- ------------------------------------------------------------

CREATE TABLE tblGroupMemberships (
  ID INTEGER  NOT NULL  ,
  GroupID INTEGER  NOT NULL  ,
  UserID INTEGER  NOT NULL    ,
PRIMARY KEY(ID),
  FOREIGN KEY(GroupID)
    REFERENCES tblGroup(ID)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(UserID)
    REFERENCES tblUser(ID)
      ON DELETE CASCADE
      ON UPDATE CASCADE);



CREATE TABLE tblVersePermissions (
  ID INTEGER  NOT NULL  ,
  VerseID INTEGER  NOT NULL  ,
  GroupID INTEGER  NOT NULL    ,
PRIMARY KEY(ID),
  FOREIGN KEY(GroupID)
    REFERENCES tblGroup(ID)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(VerseID)
    REFERENCES tblVerseMetaInfo(ID)
      ON DELETE CASCADE
      ON UPDATE CASCADE);



CREATE TABLE tblVerseCharacter (
  ID INTEGER  NOT NULL  ,
  tblVerseMetaInfo_ID INTEGER  NOT NULL  ,
  CharacterID INTEGER  NOT NULL    ,
PRIMARY KEY(ID),
  FOREIGN KEY(tblVerseMetaInfo_ID)
    REFERENCES tblVerseMetaInfo(ID)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(CharacterID)
    REFERENCES tblCharacter(ID)
      ON DELETE CASCADE
      ON UPDATE CASCADE);



CREATE TABLE tblVerseEntity (
  ID INTEGER  NOT NULL  ,
  VerseID INTEGER  NOT NULL  ,
  EntityID INTEGER  NOT NULL    ,
PRIMARY KEY(ID),
  FOREIGN KEY(VerseID)
    REFERENCES tblVerseMetaInfo(ID)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(EntityID)
    REFERENCES tblEntity(ID)
      ON DELETE CASCADE
      ON UPDATE CASCADE);



CREATE TABLE tblCharEntity (
  ID INTEGER  NOT NULL  ,
  CharacterID INTEGER  NOT NULL  ,
  EntityID INTEGER  NOT NULL  ,
  RelationType VARCHAR(255)      ,
PRIMARY KEY(ID)  ,
  FOREIGN KEY(CharacterID)
    REFERENCES tblCharacter(ID)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(EntityID)
    REFERENCES tblEntity(ID)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);


CREATE INDEX tblCharEntity_FKIndex2 ON tblCharEntity (EntityID);



CREATE TABLE tblCharacterRelations (
  ID INTEGER  NOT NULL  ,
  CharacterBID INTEGER  NOT NULL  ,
  CharacterAID INTEGER  NOT NULL  ,
  ChangeSequence INTEGER    ,
  Current BOOL    ,
  StoryRelationshipSet INT    ,
  ChapterRelationshipSet INT    ,
  RelationshipVerse INTEGER    ,
  RelationshipType VARCHAR(255)    ,
  RelationShipDesc TEXT      ,
PRIMARY KEY(ID),
  FOREIGN KEY(CharacterAID)
    REFERENCES tblCharacter(ID)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(CharacterBID)
    REFERENCES tblCharacter(ID)
      ON DELETE CASCADE
      ON UPDATE CASCADE);







CREATE TABLE tblChapterCharacter (
  ID INTEGER  NOT NULL  ,
  CharacterID INTEGER  NOT NULL  ,
  ChapterID INTEGER  NOT NULL  ,
  Role VARCHAR(255)    ,
  HasPerspective BOOL      ,
PRIMARY KEY(ID)    ,
  FOREIGN KEY(ChapterID)
    REFERENCES tblChapter(ID)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(CharacterID)
    REFERENCES tblCharacter(ID)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);


CREATE INDEX tblChapterCharacter_FKIndex1 ON tblChapterCharacter (ChapterID);
CREATE INDEX tblChapterCharacter_FKIndex2 ON tblChapterCharacter (CharacterID);



CREATE TABLE tblFiction (
  ID INTEGER  NOT NULL  ,
  VerseID INTEGER  NOT NULL  ,
  Title VARCHAR(255)  NOT NULL  ,
  Slug TINYTEXT    ,
  Description TEXT    ,
  NumChapters INTEGER    ,
  CreatedDateTime DATETIME      ,
PRIMARY KEY(ID),
  FOREIGN KEY(VerseID)
    REFERENCES tblVerseMetaInfo(ID)
      ON DELETE CASCADE
      ON UPDATE CASCADE);



CREATE TABLE tblFictionPermissions (
  ID INTEGER  NOT NULL  ,
  FictionID INTEGER  NOT NULL  ,
  GroupID INTEGER  NOT NULL    ,
PRIMARY KEY(ID),
  FOREIGN KEY(GroupID)
    REFERENCES tblGroup(ID)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(FictionID)
    REFERENCES tblFiction(ID)
      ON DELETE CASCADE
      ON UPDATE CASCADE);



CREATE TABLE tblFicCharacter (
  ID INTEGER  NOT NULL  ,
  CharacterID INTEGER  NOT NULL  ,
  FictionID INTEGER  NOT NULL  ,
  Role VARCHAR(255)      ,
PRIMARY KEY(ID)  ,
  FOREIGN KEY(CharacterID)
    REFERENCES tblCharacter(ID)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(FictionID)
    REFERENCES tblFiction(ID)
      ON DELETE CASCADE
      ON UPDATE CASCADE);


CREATE INDEX tblFicCharacter_FKIndex2 ON tblFicCharacter (FictionID);



CREATE TABLE tblFicChapter (
  ID INTEGER  NOT NULL  ,
  ChapterID INTEGER  NOT NULL  ,
  FictionID INTEGER  NOT NULL    ,
PRIMARY KEY(ID),
  FOREIGN KEY(ChapterID)
    REFERENCES tblChapter(ID)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(FictionID)
    REFERENCES tblFiction(ID)
      ON DELETE CASCADE
      ON UPDATE CASCADE);




