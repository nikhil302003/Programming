
CREATE TABLE Bank (
    branch_id INT PRIMARY KEY,
    branch_name VARCHAR(100),
    branch_city VARCHAR(100)
);


CREATE TABLE AccountHolder (
    account_holder_id INT PRIMARY KEY,
    account_no VARCHAR(20) UNIQUE,
    account_holder_name VARCHAR(100),
    city VARCHAR(100),
    contact VARCHAR(15),
    date_of_account_created DATE,
    account_status VARCHAR(20),     
    account_type VARCHAR(50),
    balance DECIMAL(15, 2)
);


CREATE TABLE Loan (
    loan_no INT PRIMARY KEY,
    branch_id INT,
    account_holder_id INT,
    loan_amount DECIMAL(15, 2),
    loan_type VARCHAR(50),
    FOREIGN KEY (branch_id) REFERENCES Bank(branch_id),
    FOREIGN KEY (account_holder_id) REFERENCES AccountHolder(account_holder_id)
);


SET @accountA = 'A_account_no';  -- replace with actual account no
SET @accountB = 'B_account_no';  -- replace with actual account no
SET @transferAmount = 100;

START TRANSACTION;


UPDATE AccountHolder
SET balance = balance - @transferAmount
WHERE account_no = @accountA AND balance >= @transferAmount;


UPDATE AccountHolder
SET balance = balance + @transferAmount
WHERE account_no = @accountB;


COMMIT;


SELECT DISTINCT ah1.*
FROM AccountHolder ah1
JOIN AccountHolder ah2 ON ah1.city = ah2.city AND ah1.account_holder_id <> ah2.account_holder_id;


SELECT account_no, account_holder_name
FROM AccountHolder
WHERE DAY(date_of_account_created) > 15;


SELECT branch_city AS city_name, COUNT(branch_id) AS Count_Branch
FROM Bank
GROUP BY branch_city;


SELECT ah.account_holder_id, ah.account_holder_name, l.branch_id, l.loan_amount
FROM AccountHolder ah

JOIN Loan l ON ah.account_holder_id = l.account_holder_id;
