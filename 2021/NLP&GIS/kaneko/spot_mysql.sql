CREATE TABLE todofuken( -- 都道府県
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE spots(-- 観光地
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  todofuken_id INTEGER,
  title TEXT NOT NULL,-- タイトル
  lead_sentence TEXT,-- リード文
  overview TEXT,-- 概要
  longitude_latitude TEXT, -- 緯度経度
  addr TEXT, -- 住所
  note TEXT, -- 補足
  FOREIGN KEY(todofuken_id) REFERENCES todofuken(id)
);

