create table if not exists version (
    version varchar(10) not null primary key
);

insert or ignore into version values ('0.0.0');

drop table if exists Musculo;

create table Musculo (
    ID integer primary key autoincrement,
    Nombre varchar(20) not null unique
);

drop table if exists Ejercicio;

create table Ejercicio (
    ID integer primary key autoincrement,
    ID_Musculo integer not null,
    Nombre varchar(30) not null,
    foreign key(ID_Musculo) references Musculo(ID)
);

drop table if exists Entrenamiento;

create table Entrenamiento (
    ID integer primary key autoincrement,
    Fecha datetime not null
);

drop table if exists Serie;

create table Serie (
    ID integer primary key autoincrement,
    ID_Ejercicio integer not null,
    ID_Entrenamiento integer not null,
    Peso real not null check (Peso > 0),
    Repeticiones integer not null check (Repeticiones > 0),
    Tipo char(1) not null check(Tipo in ("n", "d")),
    foreign key(ID_Ejercicio) references Ejercicio(ID),
    foreign key(ID_Entrenamiento) references Entrenamiento(ID)
);

drop table if exists Rutina;

create table Rutina (
    ID integer primary key autoincrement,
    Nombre varchar(30) not null
);

drop table if exists EjerRutina;

create table EjerRutina (
    ID integer primary key autoincrement,
    ID_Rutina integer not null,
    ID_Ejercicio integer not null,
    Series integer,
    foreign key(ID_Rutina) references Rutina(ID),
    foreign key(ID_Ejercicio) references Ejercicio(ID)
);

drop view if exists V_Entrenamiento;

create view V_Entrenamiento as 
    select s.ID_Entrenamiento, e.Nombre, e.ID_Musculo, s.Peso, s.Repeticiones, s.Tipo 
    from Serie s inner join Ejercicio e on s.ID_Ejercicio = e.ID 
    order by s.ID;

drop view if exists V_Ult_Entrenamiento;

create view V_Ult_Entrenamiento as
    select max(ID) as ID from Entrenamiento;

drop view if exists V_Ejercicio;

create view V_Ejercicio as
    select e.ID as ID, e.Nombre, m.ID as IDMusculo, m.Nombre
    from Ejercicio e inner join Musculo m on e.ID_Musculo = m.ID;

drop view if exists V_Ult_Ejercicio;

create view V_Ult_Ejercicio as
    select max(ID) as ID from Ejercicio;

drop view if exists V_Ult_Entrenos_Ejercicio;

create view V_Ult_Entrenos_Ejercicio as
    select e.ID as IDEntr, e.Fecha, s.ID_Ejercicio as IDEjer
    from Entrenamiento e inner join Serie s on e.ID = s.ID_Entrenamiento
    order by e.Fecha;

drop view if exists V_Rutinas;

create view V_Rutinas as
    select t.ID_Rutina, r.Nombre as NombreRutina, t.ID_Ejercicio, e.Nombre as NombreEjer, t.Series
    from Rutina r inner join EjerRutina t on r.ID = t.ID_Rutina 
    inner join Ejercicio e on t.ID_Ejercicio = e.ID
    order by t.ID_Rutina, t.ID_Ejercicio;

drop view if exists V_Ult_Rutina;

create view V_Ult_Rutina as
    select max(ID) from Rutina;