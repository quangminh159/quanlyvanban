CREATE DATABASE qlvanban
COLLATE Vietnamese_CI_AS;
GO
USE qlvanban;
GO
CREATE TABLE users (
    id INT PRIMARY KEY IDENTITY(1,1),
    username NVARCHAR(50) COLLATE Vietnamese_CI_AS NOT NULL UNIQUE,  
    password NVARCHAR(50) COLLATE Vietnamese_CI_AS NOT NULL,         
    full_name NVARCHAR(100) COLLATE Vietnamese_CI_AS,     
    role NVARCHAR(10) COLLATE Vietnamese_CI_AS CHECK (role IN (N'Admin', N'User')),
    created_at DATETIME DEFAULT GETDATE()  
);

CREATE TABLE incomingDocuments (
    documentID INT PRIMARY KEY IDENTITY(1,1),  
    documentNumber NVARCHAR(50) COLLATE Vietnamese_CI_AS NOT NULL,  
    title NVARCHAR(255) COLLATE Vietnamese_CI_AS NOT NULL,         
    sender NVARCHAR(255) COLLATE Vietnamese_CI_AS,                
    receivedDate DATE NOT NULL,                                  
    content NVARCHAR(MAX) COLLATE Vietnamese_CI_AS,           
    attachment NVARCHAR(255) COLLATE Vietnamese_CI_AS,           
    status NVARCHAR(50) COLLATE Vietnamese_CI_AS CHECK (status IN (N'Chưa xử lý', N'Đã xử lý')) DEFAULT N'Chưa xử lý' 
);
CREATE TABLE outgoingDocuments (
    documentID INT PRIMARY KEY IDENTITY(1,1), 
    documentNumber NVARCHAR(50) COLLATE Vietnamese_CI_AS NOT NULL,  
    title NVARCHAR(255) COLLATE Vietnamese_CI_AS NOT NULL,         
    recipient NVARCHAR(255) COLLATE Vietnamese_CI_AS,          
    sentDate DATE NOT NULL,                                      
    content NVARCHAR(MAX) COLLATE Vietnamese_CI_AS,             
    attachment NVARCHAR(255) COLLATE Vietnamese_CI_AS,       
    status NVARCHAR(50) COLLATE Vietnamese_CI_AS CHECK (status IN (N'Đã gửi', N'Đang gửi', N'Hủy bỏ')) DEFAULT N'Đã gửi'
);
CREATE TABLE taskFiles (
    fileID INT PRIMARY KEY IDENTITY(1,1),              
    fileName NVARCHAR(255) COLLATE Vietnamese_CI_AS NOT NULL, 
    description NVARCHAR(MAX) COLLATE Vietnamese_CI_AS,        
    createdDate DATE DEFAULT CURRENT_TIMESTAMP,             
    status NVARCHAR(50) COLLATE Vietnamese_CI_AS CHECK (status IN (N'Đang thực hiện', N'Hoàn thành')) DEFAULT N'Đang thực hiện'
);
CREATE TABLE sharedDocuments (
    documentID INT PRIMARY KEY IDENTITY(1,1),           
    documentName NVARCHAR(255) COLLATE Vietnamese_CI_AS NOT NULL, 
    description NVARCHAR(MAX) COLLATE Vietnamese_CI_AS,          
    uploadedDate DATE DEFAULT CURRENT_TIMESTAMP,               
    documentFile NVARCHAR(255) COLLATE Vietnamese_CI_AS,      
    uploadedBy NVARCHAR(100) COLLATE Vietnamese_CI_AS      
);
CREATE TABLE categories (
    categoryID INT PRIMARY KEY IDENTITY(1,1),           
    categoryName NVARCHAR(255) COLLATE Vietnamese_CI_AS NOT NULL, 
    description NVARCHAR(MAX) COLLATE Vietnamese_CI_AS           
);
CREATE TABLE informationExtraction (
    extractionID INT PRIMARY KEY IDENTITY(1,1),
    performedBy NVARCHAR(100) COLLATE Vietnamese_CI_AS NOT NULL,  
    informationType NVARCHAR(255) COLLATE Vietnamese_CI_AS,     
    date DATE DEFAULT CURRENT_TIMESTAMP,                        
    result NVARCHAR(MAX) COLLATE Vietnamese_CI_AS                
);
CREATE TABLE activityLog (
    logID INT PRIMARY KEY IDENTITY(1,1),               
    performedBy NVARCHAR(100) COLLATE Vietnamese_CI_AS,
    action NVARCHAR(255) COLLATE Vietnamese_CI_AS,     
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,      
    details NVARCHAR(MAX) COLLATE Vietnamese_CI_AS    
);
INSERT INTO users (username, password, full_name, role)
VALUES 
    ('nvana', '123', N'Nguyễn Minh Quân', 'Admin');
INSERT INTO incomingDocuments (documentNumber, title, sender, receivedDate, content, attachment, status)
VALUES ('001/2024', N'Thông báo họp', N'Ban giám đốc', '2024-11-26', N'Thông báo họp về dự án mới', 'attachment.pdf', N'Chưa xử lý');

INSERT INTO outgoingDocuments (documentNumber, title, recipient, sentDate, content, attachment, status)
VALUES ('002/2024', N'Thông báo nghỉ lễ', N'Công ty XYZ', '2024-11-25', N'Thông báo nghỉ lễ vào cuối tuần', 'holiday_notice.pdf', N'Đã gửi');

INSERT INTO taskFiles (fileName, description, createdDate, status)
VALUES (N'Hồ sơ dự án A', N'Hồ sơ liên quan đến dự án A', '2024-11-26', N'Đang thực hiện');

INSERT INTO sharedDocuments (documentName, description, uploadedDate, documentFile, uploadedBy)
VALUES (N'Báo cáo tài chính Q1', N'Báo cáo tài chính quý 1', '2024-11-20', 'financial_report_q1.pdf', N'Nguyen Thi Ánh');

INSERT INTO categories (categoryName, description)
VALUES (N'Văn bản quan trọng', N'Danh mục các văn bản quan trọng cần xử lý nhanh');

INSERT INTO informationExtraction (performedBy, informationType, date, result)
VALUES (N'Nguyen Thi B', N'Kết quả khảo sát', '2024-11-25', N'Kết quả khảo sát cho thấy dự án cần cải tiến');

INSERT INTO activityLog (performedBy, action, timestamp, details)
VALUES (N'Nguyen Thi B', N'Thêm văn bản mới', '2024-11-26 10:30:00', N'Thêm văn bản "Thông báo họp" vào hệ thống');

UPDATE users
SET password = 'newpassword123', role = 'User'
WHERE username = 'nvana';

UPDATE incomingDocuments
SET status = N'Đã xử lý'
WHERE documentID = 1;

UPDATE outgoingDocuments
SET status = N'Đã gửi'
WHERE documentID = 2;

UPDATE taskFiles
SET status = N'Hoàn thành'
WHERE fileID = 1;

UPDATE sharedDocuments
SET documentFile = 'updated_report.pdf'
WHERE documentID = 1;

UPDATE categories
SET description = N'Danh mục dành cho các văn bản khẩn cấp'
WHERE categoryID = 1;

UPDATE informationExtraction
SET result = N'Dự án đã cải tiến theo khảo sát'
WHERE extractionID = 1;

UPDATE activityLog
SET details = N'Cập nhật văn bản quan trọng'
WHERE logID = 1;

DELETE FROM users
WHERE username = 'nvana';

DELETE FROM incomingDocuments
WHERE documentID = 1;

DELETE FROM outgoingDocuments
WHERE documentID = 2;

DELETE FROM taskFiles
WHERE fileID = 1;

DELETE FROM sharedDocuments
WHERE documentID = 1;

DELETE FROM categories
WHERE categoryID = 1;

DELETE FROM informationExtraction
WHERE extractionID = 1;

DELETE FROM activityLog
WHERE logID = 1;

SELECT * FROM users;

SELECT * FROM incomingDocuments;

SELECT * FROM outgoingDocuments;

SELECT * FROM taskFiles;

SELECT * FROM sharedDocuments;

SELECT * FROM categories;

SELECT * FROM informationExtraction;

SELECT * FROM activityLog;