DROP TABLE IF EXISTS user_table;
DROP TABLE IF EXISTS suspension_table;
DROP TABLE IF EXISTS message_table;
DROP TABLE IF EXISTS community_table;
DROP TABLE IF EXISTS channel_table;
DROP TABLE IF EXISTS dm_table;

CREATE TABLE user_table(
    ID SERIAL,
    username VARCHAR(255),
    password VARCHAR(255),
    session_key VARCHAR(255)
);

CREATE TABLE message_table(
    messageID INTEGER NOT NULL,
    message VARCHAR(255),
    date VARCHAR(255),
    time VARCHAR(255),
    sender VARCHAR(255),
    receiver VARCHAR(255),
    comm_name VARCHAR(255),
    chan_name VARCHAR(255)
);

CREATE TABLE community_table(
    name VARCHAR(255),
    users VARCHAR(255),
    channels VARCHAR(255)
);

CREATE TABLE channel_table(
    community_name VARCHAR(255),
    channel_name VARCHAR(255),
    date VARCHAR(255),
    time VARCHAR(255),
    sender VARCHAR(255),
    message VARCHAR(255)
);

CREATE TABLE dm_table(
    message VARCHAR(255),
    date VARCHAR(255),
    time VARCHAR(255),
    sender VARCHAR(255),
    receiver VARCHAR(255)
);

INSERT INTO user_table(username) 
VALUES 
    ('Abbott'),
    ('Costello'),
    ('Moe'),
    ('Larry'),
    ('Curly'),
    ('DrMarvin');


INSERT INTO message_table(messageID, message, date, time, sender, receiver, comm_name, chan_name) 
VALUES 
    ('1','Hello Costello! How are you today?', '06-05-1922', '2:05 PM','Abbott', 'Costello', 'Comedy', '#Dialogs'),
    ('2','Hello Abbott. Long time, no see.', '06-05-1922', '2:33 PM','Costello', 'Abbott', 'Comedy', '#Dialogs'),
    ('3','Where is the money, Larry? It is the twentieth of the month.', '12-20-1968', '8:46 PM','Moe', 'Larry', 'Comedy', '#ArgumentClinic'),
    ('4','I do not care, Moe. You know this, pal.', '12-20-1968', '9:08 PM', 'Larry', 'Moe', 'Comedy', '#ArgumentClinic'),
    ('5','55 years later, and you still look great, Costello!', '07-20-1977', '7:08 AM','Curly', 'Costello', 'Comedy', '#ArgumentClinic'),
    ('2','Let me tell you, I am on cloud 9.', '07-20-1977', '7:11 AM','Costello', 'Curly', 'Comedy', '#ArgumentClinic'),
    ('5','Good for you, little man!', '07-20-1977', '7:15 AM','Curly', 'Costello', 'Comedy', '#ArgumentClinic');


INSERT INTO dm_table(message, date, time, sender, receiver)
VALUES
    ('Hello Costello! How are you today?', '06-05-1922', '2:05 PM','Abbott', 'Costello'),
    ('Hello Abbott. Long time, no see.', '06-05-1922', '2:33 PM','Costello', 'Abbott'),
    ('Where is the money, Larry? It is the twentieth of the month.', '12-20-1968', '8:46 PM','Moe', 'Larry'),
    ('I do not care, Moe. You know this, pal.', '12-20-1968', '9:08 PM', 'Larry', 'Moe'),
    ('55 years later, and you still look great, Costello!', '07-20-1977', '7:08 AM','Curly', 'Costello'),
    ('Let me tell you, I am on cloud 9.', '07-20-1977', '7:11 AM','Costello', 'Curly'),
    ('Good for you, little man!', '07-20-1977', '7:15 AM','Curly', 'Costello');


INSERT INTO community_table(name, users, channels) 
VALUES 
    ('Arrakis', 'spicelover', '#Worms,#Random'),
    ('Comedy', 'Abbott,Costello,Moe,Larry,Curly,DrMarvin,BabySteps2Door', '#ArgumentClinic,#Dialogs');

INSERT INTO channel_table(community_name, channel_name, date, time, sender, message) 
VALUES 
    ('Comedy','#ArgumentClinic', '01-20-1961', '5:32 AM', 'Abbott', 'Good Morning! Good Morning!'),
    ('Comedy','#ArgumentClinic', '01-20-1961', '5:45 AM', 'Moe', 'Hi Abbott!'),
    ('Comedy','#Dialogs', '10-01-2023', '9:45 AM', 'Moe', 'please reply'),
    ('Comedy','#Dialogs', '10-01-2023', '9:55 AM', 'Abbott', 'i replied already!');
