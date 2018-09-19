USE orders;
CREATE TABLE order_requests (
  id int(11) unsigned NOT NULL AUTO_INCREMENT,
  origin_lat float NOT NULL,
  origin_lon float NOT NULL,
  destination_lat float NOT NULL,
  destination_lon float NOT NULL,
  distance int(11) NOT NULL,
  createdate int(11) NOT NULL,
  status int(2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

