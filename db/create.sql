-- enterprise create
DROP TABLES IF EXISTS `enterprise`;

CREATE TABLE `enterprise`.`enterprise` (
	`id` bigint NOT NULL AUTO_INCREMENT COMMENT 'ID',
	`name` varchar(100) COMMENT '企业名称',
	`email` varchar(55) COMMENT '邮箱',
	`phone` varchar(55) COMMENT '电话',
	`tyc_url` varchar(100) COMMENT '天眼查URL',
	`company_url` varchar(100) COMMENT '公司官网',
	`address` varchar(255) COMMENT '地址',
	`register_funds` varchar(20) COMMENT '注册资金',
	`paidin_funds` varchar(20) COMMENT '实缴资金',
	`establish_date` date COMMENT '注册日期',
	`status` varchar(30) COMMENT '经营状态',
	`credit_code` varchar(30) NOT NULL COMMENT '信用代码',
	`company_type` varchar(30) COMMENT '公司类型',
	`industry` varchar(100) COMMENT '所属行业',
	`business_term` varchar(55) COMMENT '营业期限',
	`resume` text COMMENT '简述',
	`business_scope` text COMMENT '经营范围',
	`key` varchar(55) COMMENT '搜索关键字',
	PRIMARY KEY (`id`, `credit_code`)
) COMMENT='企业信息表';

-- citys create
DROP TABLES IF EXISTS `citys`;

CREATE TABLE `enterprise`.`citys` (
	`id` int NOT NULL COMMENT 'ID',
	`name` varchar(100) COMMENT '简称',
	`full_name` varchar(100) COMMENT '全名称',
	`parent_id` int COMMENT '父ID',
	`code` varchar(30) COMMENT 'code',
	`is_cg` bool COMMENT '是否直辖市',
	PRIMARY KEY (`id`)
) COMMENT='区域信息表';