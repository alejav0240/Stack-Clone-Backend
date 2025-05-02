create table achievements_achievement (
  id integer not null primary key autoincrement,
  name varchar(255) not null unique,
  description text not null
);

create table articles_status (
  id integer not null primary key autoincrement,
  name varchar(255) not null unique
);

create table auth_group (
  id integer not null primary key autoincrement,
  name varchar(150) not null unique
);

create table django_content_type (
  id integer not null primary key autoincrement,
  app_label varchar(100) not null,
  model varchar(100) not null
);

create table auth_permission (
  id integer not null primary key autoincrement,
  content_type_id integer not null references django_content_type,
  codename varchar(100) not null,
  name varchar(255) not null
);

create table auth_group_permissions (
  id integer not null primary key autoincrement,
  group_id integer not null references auth_group,
  permission_id integer not null references auth_permission
);
create index auth_group_permissions_group_id_b120cbf9 on auth_group_permissions (group_id);
create unique index auth_group_permissions_group_id_permission_id_0cd325b0_uniq on auth_group_permissions (group_id, permission_id);
create index auth_group_permissions_permission_id_84c5c92e on auth_group_permissions (permission_id);

create index auth_permission_content_type_id_2f476e4b on auth_permission (content_type_id);
create unique index auth_permission_content_type_id_codename_01ab375a_uniq on auth_permission (content_type_id, codename);

create unique index django_content_type_app_label_model_76bd3d3b_uniq on django_content_type (app_label, model);

create table django_migrations (
  id integer not null primary key autoincrement,
  app varchar(255) not null,
  name varchar(255) not null,
  applied datetime not null
);

create table django_session (
  session_key varchar(40) not null primary key,
  session_data text not null,
  expire_date datetime not null
);
create index django_session_expire_date_a5c62663 on django_session (expire_date);

create table tags_tag (
  id integer not null primary key autoincrement,
  name varchar(255) not null unique,
  active bool not null
);

create table users_rank (
  id integer not null primary key autoincrement,
  name varchar(255) not null unique,
  min_points integer not null
);

create table users_customuser (
  id integer not null primary key autoincrement,
  password varchar(128) not null,
  last_login datetime,
  is_superuser bool not null,
  username varchar(150) not null unique,
  first_name varchar(150) not null,
  last_name varchar(150) not null,
  email varchar(254) not null,
  is_staff bool not null,
  is_active bool not null,
  date_joined datetime not null,
  age integer,
  rol varchar(50) not null,
  habilitado bool not null,
  created_at datetime not null,
  rank_id bigint references users_rank,
  lastname varchar(255),
  name varchar(255)
);

create table achievements_userachievement (
  id integer not null primary key autoincrement,
  achieved_at datetime not null,
  achievement_id bigint not null references achievements_achievement,
  user_id bigint not null references users_customuser
);
create index achievements_userachievement_achievement_id_47ecf9c2 on achievements_userachievement (achievement_id);
create index achievements_userachievement_user_id_8e205b1b on achievements_userachievement (user_id);

create table articles_article (
  id integer not null primary key autoincrement,
  title text not null,
  body text not null,
  created_at datetime not null,
  user_id bigint not null references users_customuser,
  status_id bigint references articles_status
);
create index articles_article_status_id_6ca2c41d on articles_article (status_id);
create index articles_article_user_id_6310b975 on articles_article (user_id);

create table articles_articleaudit (
  id integer not null primary key autoincrement,
  changed_at datetime not null,
  change_type varchar(255) not null,
  article_id bigint not null references articles_article
);
create index articles_articleaudit_article_id_6f5af506 on articles_articleaudit (article_id);

create table django_admin_log (
  id integer not null primary key autoincrement,
  object_id text,
  object_repr varchar(200) not null,
  action_flag smallint unsigned not null,
  change_message text not null,
  content_type_id integer references django_content_type,
  user_id bigint not null references users_customuser,
  action_time datetime not null,
  check ("action_flag" >= 0)
);
create index django_admin_log_content_type_id_c4bce8eb on django_admin_log (content_type_id);
create index django_admin_log_user_id_c564eba6 on django_admin_log (user_id);

create table points_userpoint (
  id integer not null primary key autoincrement,
  point_type varchar(20) not null,
  points integer not null,
  active bool not null,
  user_id bigint not null references users_customuser
);
create index points_userpoint_user_id_df2350c4 on points_userpoint (user_id);

create table questions_question (
  id integer not null primary key autoincrement,
  title text not null,
  body text not null,
  created_at datetime not null,
  active bool not null,
  user_id bigint not null references users_customuser
);

create table questions_answer (
  id integer not null primary key autoincrement,
  body text not null,
  created_at datetime not null,
  active bool not null,
  user_id bigint not null references users_customuser,
  question_id bigint not null references questions_question
);
create index questions_answer_question_id_45884d67 on questions_answer (question_id);
create index questions_answer_user_id_b3ad5f22 on questions_answer (user_id);

create index questions_question_user_id_e2ae6bb3 on questions_question (user_id);

create table questions_question_tags (
  id integer not null primary key autoincrement,
  question_id bigint not null references questions_question,
  tag_id bigint not null references tags_tag
);
create index questions_question_tags_question_id_1fab941d on questions_question_tags (question_id);
create unique index questions_question_tags_question_id_tag_id_bb41947a_uniq on questions_question_tags (question_id, tag_id);
create index questions_question_tags_tag_id_72ee1cba on questions_question_tags (tag_id);

create index users_customuser_rank_id_a7a4cf0d on users_customuser (rank_id);

create table users_customuser_groups (
  id integer not null primary key autoincrement,
  customuser_id bigint not null references users_customuser,
  group_id integer not null references auth_group
);
create index users_customuser_groups_customuser_id_958147bf on users_customuser_groups (customuser_id);
create unique index users_customuser_groups_customuser_id_group_id_76b619e3_uniq on users_customuser_groups (customuser_id, group_id);
create index users_customuser_groups_group_id_01390b14 on users_customuser_groups (group_id);

create table users_customuser_user_permissions (
  id integer not null primary key autoincrement,
  customuser_id bigint not null references users_customuser,
  permission_id integer not null references auth_permission
);
create index users_customuser_user_permissions_customuser_id_5771478b on users_customuser_user_permissions (customuser_id);
create unique index users_customuser_user_permissions_customuser_id_permission_id_7a7debf6_uniq on users_customuser_user_permissions (customuser_id, permission_id);
create index users_customuser_user_permissions_permission_id_baaa2f74 on users_customuser_user_permissions (permission_id);

create table votes_vote (
  id integer not null primary key autoincrement,
  vote_type varchar(10) not null,
  created_at datetime not null,
  active bool not null,
  answer_id bigint references questions_answer,
  article_id bigint references articles_article,
  question_id bigint references questions_question,
  user_id bigint not null references users_customuser
);
create index votes_vote_answer_id_3553ad73 on votes_vote (answer_id);
create index votes_vote_article_id_cb6122fb on votes_vote (article_id);
create index votes_vote_question_id_fad731b0 on votes_vote (question_id);
create index votes_vote_user_id_24a74629 on votes_vote (user_id);