-- 删除已存在的表（如果有）
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS fixed_events;

-- 创建课程表
CREATE TABLE courses (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    teacher TEXT,
    location TEXT,
    day TEXT NOT NULL,  -- 存储逗号分隔的天数，如"1,3,5"
    time TEXT NOT NULL, -- 存储逗号分隔的小时，如"9,10"
    color TEXT NOT NULL,
    type TEXT NOT NULL DEFAULT 'course',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建固定事件表
CREATE TABLE fixed_events (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    day TEXT NOT NULL,
    time TEXT NOT NULL,
    color TEXT NOT NULL,
    type TEXT NOT NULL,
    teacher TEXT,
    location TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 插入固定事件数据
INSERT INTO fixed_events (id, name, day, time, color, type, location) VALUES
('breakfast', '早餐', '1,2,3,4,5,6,7', '7', 'bg-amber-100 dark:bg-amber-900 text-amber-800 dark:text-amber-100', 'meal', '食堂'),
('lunch', '午餐', '1,2,3,4,5,6,7', '12', 'bg-amber-100 dark:bg-amber-900 text-amber-800 dark:text-amber-100', 'meal', '食堂'),
('dinner', '晚餐', '1,2,3,4,5,6,7', '18', 'bg-amber-100 dark:bg-amber-900 text-amber-800 dark:text-amber-100', 'meal', '食堂'),
('eveningstudy', '晚修', '1,2,3,4,5', '19,20,21', 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-100', 'study', '教室');

-- 插入一些示例课程数据
INSERT INTO courses (id, name, teacher, location, day, time, color, type) VALUES
('math', '数学', '王老师', '教室101', '1,3,5', '9', 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-100', 'course'),
('english', '英语', '李老师', '教室102', '2,4', '9', 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-100', 'course'),
('physics', '物理', '张老师', '实验室201', '1,3', '10', 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-100', 'course'),
('chemistry', '化学', '陈老师', '实验室202', '2,4', '10', 'bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-100', 'course'),
('history', '历史', '刘老师', '教室103', '1,5', '13', 'bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-100', 'course'),
('geography', '地理', '赵老师', '教室104', '2,4', '13', 'bg-indigo-100 dark:bg-indigo-900 text-indigo-800 dark:text-indigo-100', 'course'),
('biology', '生物', '孙老师', '实验室203', '3,5', '14', 'bg-emerald-100 dark:bg-emerald-900 text-emerald-800 dark:text-emerald-100', 'course'),
('pe', '体育', '周老师', '操场', '1,3', '16', 'bg-orange-100 dark:bg-orange-900 text-orange-800 dark:text-orange-100', 'course'),
('art', '美术', '吴老师', '美术室', '2', '16', 'bg-rose-100 dark:bg-rose-900 text-rose-800 dark:text-rose-100', 'course'),
('music', '音乐', '郑老师', '音乐室', '4', '16', 'bg-pink-100 dark:bg-pink-900 text-pink-800 dark:text-pink-100', 'course');