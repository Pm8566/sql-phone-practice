CREATE TABLE assets (
asset_id	INTEGER PRIMARY KEY,
serial 		TEXT NOT NULL,
asset_type	TEXT,
brand		TEXT,
received_date	TEXT,
status		TEXT,
value_gbp	REAL
);

INSERT INTO assets VALUES
(1,'SN1001','Laptop','Dell','2026-09-01','Erased',120),
(2,'SN1002','Laptop','HP','2026-09-01','Awaiting erasure',95),
(3,'SN1003','Desktop','Lenovo','2026-09-03','Recycled',0),
(4,'SN1004','Phone','Apple','2026-09-05','Erased',180),
(5,'SN1005','Server','Dell','2026-09-08','Awaiting erasure',300),
(6,'SN1006','Laptop','Lenovo','2026-09-10','Resold',150),
(7,'SN1007','Phone','Samsung','2026-09-10','Erased',70),
(8,'SN1008','Desktop','HP','2026-09-12','Resold',60);
