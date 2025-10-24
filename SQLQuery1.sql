
-- 1. T?O B?NG 'users'
CREATE TABLE users (
    -- Dùng UNIQUEIDENTIFIER làm ki?u d? li?u cho ID, và ??t giá tr? m?c ??nh là m?t UUID m?i
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),

    -- Dùng NVARCHAR ?? h? tr? t?t các ký t? Unicode (nh? ti?ng Vi?t)
    email NVARCHAR(255) NOT NULL UNIQUE,
    password_hash NVARCHAR(255) NOT NULL,
    full_name NVARCHAR(255),
    phone_number NVARCHAR(20) UNIQUE,

    -- Thay th? cho ENUM c?a MySQL: Dùng NVARCHAR và m?t ràng bu?c CHECK
    -- ?? ??m b?o giá tr? ch? có th? là 'passenger' ho?c 'driver'
    user_type NVARCHAR(10) NOT NULL CHECK (user_type IN ('passenger', 'driver')),

    -- Dùng DATETIME2 là ki?u d? li?u ngày gi? tiêu chu?n, chính xác cao
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE()
);
GO -- D?u ng?t l?nh trong T-SQL

-- 2. T?O TRIGGER ?? T? ??NG C?P NH?T TR??NG 'updated_at'
CREATE TRIGGER trg_users_update_timestamp
ON users          -- Trigger này áp d?ng cho b?ng 'users'
AFTER UPDATE      -- Nó s? ???c kích ho?t SAU KHI có l?nh UPDATE
AS
BEGIN
    -- C?p nh?t c?t 'updated_at' thành th?i gian hi?n t?i
    -- cho t?t c? các dòng v?a ???c thay ??i (n?m trong b?ng t?m 'inserted')
    UPDATE u
    SET updated_at = GETDATE()
    FROM users u
    INNER JOIN inserted i ON u.id = i.id;
END;
GO

PRINT 'B?ng "users" và trigger "trg_users_update_timestamp" ?ã ???c t?o thành công!';
SELECT * FROM users;