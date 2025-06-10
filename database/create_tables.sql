CREATE TABLE Attendance (
    id INT IDENTITY(1,1) PRIMARY KEY,
    student_id NVARCHAR(100),
    timestamp DATETIME
);
