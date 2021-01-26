INSERT INTO pts_request_group_workspace (name) VALUES ('P/I SERIES');
INSERT INTO pts_request_group_workspace (name) VALUES ('EARLY BUILD');
INSERT INTO pts_request_group_workspace (name) VALUES ('CSC');

INSERT INTO pts_request_status (name) VALUES ('OPEN');
INSERT INTO pts_request_status (name) VALUES ('TRANSIT');
INSERT INTO pts_request_status (name) VALUES ('RECIVE');
INSERT INTO pts_request_status (name) VALUES ('RETURN');
INSERT INTO pts_request_status (name) VALUES ('PENDING');
INSERT INTO pts_request_status (name) VALUES ('CLOSE');
INSERT INTO pts_request_status (name) VALUES ('CANCEL');
INSERT INTO pts_request_status (name) VALUES ('GOOD');
INSERT INTO pts_request_status (name) VALUES ('BAD');
INSERT INTO pts_request_status (name) VALUES ('VALIDANDO INVENTARIO');
INSERT INTO pts_request_status (name) VALUES ('SOLICITADO A OTRA AREA');
INSERT INTO pts_request_status (name) VALUES ('CORTO REAL');
INSERT INTO pts_request_status (name) VALUES ('SOLICITADO A DE GEODIS');
INSERT INTO pts_request_status (name) VALUES ('NUMERO DE PARTE NO EXISTE');

INSERT INTO pts_request_not_ncm (name) VALUES ('INSTALADO EN OTRA WU');
INSERT INTO pts_request_not_ncm (name) VALUES ('REVISION CON EL ME');

INSERT INTO users_departament (name) VALUES ('PRUEBAS');
INSERT INTO users_departament (name) VALUES ('CONTROL DE MATERIALES');
INSERT INTO users_departament (name) VALUES ('CSC');

INSERT INTO users_job (name) VALUES ('TA');
INSERT INTO users_job (name) VALUES ('TA TRAINER');
INSERT INTO users_job (name) VALUES ('TA IBM');
INSERT INTO users_job (name) VALUES ('TA LEAD');
INSERT INTO users_job (name) VALUES ('TT');
INSERT INTO users_job (name) VALUES ('IPIC');
INSERT INTO users_job (name) VALUES ('IPIC NCM');
INSERT INTO users_job (name) VALUES ('IPIC LEAD');

INSERT INTO auth_group (name) VALUES ('TA');
INSERT INTO auth_group (name) VALUES ('TT');
INSERT INTO auth_group (name) VALUES ('IPIC');
INSERT INTO auth_group (name) VALUES ('IPIC NCM');
