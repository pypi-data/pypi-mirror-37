CREATE TABLE sites (
  name VARCHAR (128) UNIQUE
);

CREATE INDEX sites_name ON sites(name);

CREATE TABLE runs (
  site INTEGER,
  started DATETIME DEFAULT (DATETIME('NOW', 'LOCALTIME')),
  finished DATETIME DEFAULT NULL,
  FOREIGN KEY(site) REFERENCES sites(rowid)  
);

CREATE TABLE empty_directories (
  site INTEGER,
  run INTEGER,
  name VARCHAR (512) NOT NULL,
  mtime DATETIME NOT NULL,
  entered DATETIME DEFAULT (DATETIME('NOW', 'LOCALTIME')),
  FOREIGN KEY(site) REFERENCES sites(rowid),
  FOREIGN KEY(run) REFERENCES runs(rowid),
  UNIQUE(site, name)
);

CREATE INDEX empty_directories_site ON empty_directories(site);

CREATE TABLE empty_directories_history (
  site INTEGER,
  run INTEGER,
  name VARCHAR (512) NOT NULL,
  mtime DATETIME NOT NULL,
  entered DATETIME NOT NULL,
  acted DATETIME,
  FOREIGN KEY(site) REFERENCES sites(rowid),
  FOREIGN KEY(run) REFERENCES runs(rowid)
);

CREATE INDEX empty_directories_history_site ON empty_directories_history(site);

CREATE TABLE directories (
  name VARCHAR (512) UNIQUE
);

CREATE INDEX directories_name ON directories(name);

CREATE TABLE invalid (
  site INTEGER,
  run INTEGER,
  directory INTEGER NOT NULL,
  name VARCHAR (64) NOT NULL,
  size BIGINT NOT NULL,
  mtime DATETIME NOT NULL,
  entered DATETIME DEFAULT (DATETIME('NOW', 'LOCALTIME')),
  FOREIGN KEY(site) REFERENCES sites(rowid),
  FOREIGN KEY(run) REFERENCES runs(rowid),
  FOREIGN KEY(directory) REFERENCES directories(rowid),
  UNIQUE(site, directory, name)
);

CREATE INDEX invalid_site ON invalid(site);

CREATE TABLE invalid_history (
  site INTEGER,
  run INTEGER,
  directory INTEGER NOT NULL,
  name VARCHAR (64) NOT NULL,
  size BIGINT NOT NULL,
  mtime DATETIME NOT NULL,
  entered DATETIME NOT NULL,
  acted DATETIME,
  FOREIGN KEY(site) REFERENCES sites(rowid),
  FOREIGN KEY(run) REFERENCES runs(rowid),
  FOREIGN KEY(directory) REFERENCES directories(rowid)
);

CREATE INDEX invalid_history_site ON invalid_history(site);

CREATE TABLE orphans (
  site INTEGER,
  run INTEGER,
  directory INTEGER NOT NULL,
  name VARCHAR (64) NOT NULL,
  size BIGINT NOT NULL,
  mtime DATETIME NOT NULL,
  entered DATETIME DEFAULT (DATETIME('NOW', 'LOCALTIME')),
  FOREIGN KEY(site) REFERENCES sites(rowid),
  FOREIGN KEY(run) REFERENCES runs(rowid),
  FOREIGN KEY(directory) REFERENCES directories(rowid),
  UNIQUE(site, directory, name)
);

CREATE INDEX orphans_site ON orphans(site);

CREATE TABLE orphans_history (
  site INTEGER,
  run INTEGER,
  directory INTEGER NOT NULL,
  name VARCHAR (64) NOT NULL,
  size BIGINT NOT NULL,
  mtime DATETIME NOT NULL,
  entered DATETIME NOT NULL,
  acted DATETIME,
  FOREIGN KEY(site) REFERENCES sites(rowid),
  FOREIGN KEY(run) REFERENCES runs(rowid),
  FOREIGN KEY(directory) REFERENCES directories(rowid)
);

CREATE INDEX orphans_history_site ON orphans_history(site);

CREATE TABLE unmerged (
  site INTEGER,
  run INTEGER,
  directory INTEGER NOT NULL,
  name VARCHAR (64) NOT NULL,
  size BIGINT NOT NULL,
  mtime DATETIME NOT NULL,
  entered DATETIME DEFAULT (DATETIME('NOW', 'LOCALTIME')),
  FOREIGN KEY(site) REFERENCES sites(rowid),
  FOREIGN KEY(run) REFERENCES runs(rowid),
  FOREIGN KEY(directory) REFERENCES directories(rowid),
  UNIQUE(site, directory, name)
);

CREATE INDEX unmerged_site ON unmerged(site);

CREATE TABLE unmerged_history (
  site INTEGER,
  run INTEGER,
  directory INTEGER NOT NULL,
  name VARCHAR (64) NOT NULL,
  size BIGINT NOT NULL,
  mtime DATETIME NOT NULL,
  entered DATETIME NOT NULL,
  acted DATETIME,
  FOREIGN KEY(site) REFERENCES sites(rowid),
  FOREIGN KEY(run) REFERENCES runs(rowid),
  FOREIGN KEY(directory) REFERENCES directories(rowid)
);

CREATE INDEX unmerged_history_site ON unmerged_history(site);
