

ADD CONSTRAINT fk_teacher_class
FOREIGN KEY (teacherid) REFERENCES teacher(id)

alter table student
ADD CONSTRAINT fk_class_student
FOREIGN KEY (classid) REFERENCES class(id)

alter table classlesson
ADD CONSTRAINT fk_teacher_classlesson
FOREIGN KEY (teacherid) REFERENCES teacher(id)

alter table classlesson
ADD CONSTRAINT fk_class_classlesson
FOREIGN KEY (classid) REFERENCES class(id)

alter table classlesson
ADD CONSTRAINT fk_lesson_classlesson
FOREIGN KEY (lessonid) REFERENCES lesson(id)