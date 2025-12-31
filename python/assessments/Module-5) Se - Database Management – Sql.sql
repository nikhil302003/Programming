

CREATE TABLE Bank (
    branch_id INT PRIMARY KEY,
    branch_name VARCHAR(50),
    city VARCHAR(50)
);


CREATE TABLE AccountHolder (
    id INT PRIMARY KEY,
    account_no VARCHAR(20),
    name VARCHAR(50),
    city VARCHAR(50),
    balance DECIMAL(10,2),
    account_created DATE
);


CREATE TABLE Loan (
    loan_id INT PRIMARY KEY,
    branch_id INT,
    account_id INT,
    loan_amount DECIMAL(10,2),
    loan_type VARCHAR(30),

    FOREIGN KEY (branch_id) REFERENCES Bank(branch_id),
    FOREIGN KEY (account_id) REFERENCES AccountHolder(id)
);


START TRANSACTION;

UPDATE AccountHolder
SET balance = balance - 100
WHERE account_no = 'A001';

UPDATE AccountHolder
SET balance = balance + 100
WHERE account_no = 'B001';

COMMIT;


SELECT *
FROM AccountHolder
WHERE city IN (
    SELECT city
    FROM AccountHolder
    GROUP BY city
    HAVING COUNT(*) > 1
);


SELECT account_no, name
FROM AccountHolder
WHERE DAY(account_created) > 15;


SELECT city, COUNT(*) AS total_branches
FROM Bank
GROUP BY city;


SELECT a.id, a.name, l.loan_amount
FROM AccountHolder a
JOIN Loan l
ON a.id = l.account_id;


