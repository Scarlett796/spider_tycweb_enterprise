

-- enterprise create
-- DROP TABLES IF EXISTS `enterprise`;

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
	`create_time` timestamp COMMENT '创建时间',
	`city` varchar(55) COMMENT '省份',
	`sub_city` varchar(55) COMMENT '城市',
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

-- insert citys 直辖市、省、自治区
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(1, 'China', '中华人民共和国', 0, '', FALSE),
(2, 'bj', '北京市', 1, '', FALSE),
(3, 'sh', '上海市', 1, '', FALSE),
(4, 'tj', '天津市', 1, '', FALSE),
(5, 'cq', '重庆市', 1, '', FALSE),
(6, 'heb', '河北省', 1, '', FALSE),
(7, 'sx', '山西省', 1, '', FALSE),
(8, 'nmg', '内蒙古自治区', 1, '', FALSE),
(9, 'ln', '辽宁省', 1, '', FALSE),
(10, 'jl', '吉林省', 1, '', FALSE),
(11, 'hlj', '黑龙江省', 1, '', FALSE),
(12, 'js', '江苏省', 1, '', FALSE),
(13, 'zj', '浙江省', 1, '', FALSE),
(14, 'ah', '安徽省', 1, '', FALSE),
(15, 'fj', '福建省', 1, '', FALSE),
(16, 'jx', '江西省', 1, '', FALSE),
(17, 'sd', '山东省', 1, '', FALSE),
(18, 'hen', '河南省', 1, '', FALSE),
(19, 'hub', '湖北省', 1, '', FALSE),
(20, 'hun', '湖南省', 1, '', FALSE),
(21, 'gd', '广东省', 1, '', FALSE),
(22, 'gx', '广西壮族自治区', 1, '', FALSE),
(23, 'sz', '四川省', 1, '', FALSE),
(24, 'gz', '贵州省', 1, '', FALSE),
(25, 'yn', '云南省', 1, '', FALSE),
(26, 'han', '海南省', 1, '', FALSE),
(27, 'snx', '陕西省', 1, '', FALSE),
(28, 'gs', '甘肃省', 1, '', FALSE),
(29, 'nx', '宁夏回族自治区', 1, '', FALSE),
(30, 'qh', '青海省', 1, '', FALSE),
(31, 'xj', '新疆维吾尔自治区', 1, '', FALSE),
(32, 'xz', '西藏自治区', 1, '', FALSE),
(33, 'hk', '香港特别行政区', 1, '', TRUE),
(34, 'mo', '澳门特别行政区', 1, '', TRUE),
(35, 'tw', '台湾省', 1, '', TRUE);


-- 北京
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(36, '东城区', '东城区', 2,'110101', FALSE),
(37, '西城区', '西城区', 2,'110102', FALSE),
(38, '朝阳区', '朝阳区', 2,'110105', FALSE),
(39, '丰台区', '丰台区', 2,'110106', FALSE),
(40, '石景山区', '石景山区', 2,'110107', FALSE),
(41, '海淀区', '海淀区', 2,'110108', FALSE),
(42, '门头沟区', '门头沟区',2, '110109', FALSE),
(43, '房山区', '房山区',2, '110111', FALSE),
(44, '通州区', '通州区',2, '110112', FALSE),
(45, '顺义区', '顺义区',2, '110113', FALSE),
(46, '昌平区', '昌平区',2, '110114', FALSE),
(47, '大兴区', '大兴区',2, '110115', FALSE),
(48, '怀柔区', '怀柔区',2, '110116', FALSE),
(49, '平谷区', '平谷区',2, '110117', FALSE),
(50, '密云区', '密云区',2, '110118', FALSE),
(51, '延庆区', '延庆区',2, '110119', FALSE);
-- 上海
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(52, '黄浦区', '黄浦区', 3,'310101', FALSE),
(53, '徐汇区', '徐汇区', 3,'310104', FALSE),
(54, '长宁区', '长宁区', 3,'310105', FALSE),
(55, '静安区', '静安区', 3,'310106', FALSE),
(56, '普陀区', '普陀区', 3,'310107', FALSE),
(57, '虹口区', '虹口区', 3,'310109', FALSE),
(58, '杨浦区', '杨浦区', 3,'310110', FALSE),
(59, '闵行区', '闵行区', 3,'310112', FALSE),
(60, '宝山区', '宝山区', 3,'310113', FALSE),
(61, '嘉定区', '嘉定区', 3,'310114', FALSE),
(62, '浦东新区', '浦东新区', 3,'310115', FALSE),
(63, '金山区', '金山区', 3,'310116', FALSE),
(64, '松江区', '松江区', 3,'310117', FALSE),
(65, '青浦区', '青浦区', 3,'310118', FALSE),
(66, '奉贤区', '奉贤区', 3,'310120', FALSE),
(67, '崇明区', '崇明区', 3,'310151', FALSE);
-- 天津
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(68, '和平区', '和平区', 4,'120101', FALSE),
(69, '河东区', '河东区', 4,'120102', FALSE),
(70, '河西区', '河西区', 4,'120103', FALSE),
(71, '南开区', '南开区', 4,'120104', FALSE),
(72, '河北区', '河北区', 4,'120105', FALSE),
(73, '红桥区', '红桥区', 4,'120101', FALSE),
(74, '东丽区', '东丽区', 4,'120110', FALSE),
(75, '西青区', '西青区', 4,'120111', FALSE),
(76, '津南区', '津南区', 4,'120112', FALSE),
(77, '北辰区', '北辰区', 4,'120113', FALSE),
(78, '武清区', '武清区', 4,'120114', FALSE),
(79, '宝坻区', '宝坻区', 4,'120115', FALSE),
(80, '滨海新区', '滨海新区', 4,'120116', FALSE),
(81, '宁河区', '宁河区', 4,'120117', FALSE),
(82, '静海区', '静海区', 4,'120118', FALSE),
(83, '蓟州区', '蓟州区', 4,'120119', FALSE);
-- 重庆
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(84, '万州区', '万州区', 5,'500101', FALSE),
(85, '涪陵区', '涪陵区', 5,'500102', FALSE),
(86, '渝中区', '渝中区', 5,'500103', FALSE),
(87, '大渡口区', '大渡口区', 5,'500104', FALSE),
(88, '江北区', '江北区', 5,'500105', FALSE),
(89, '沙坪坝区', '沙坪坝区', 5,'500106', FALSE),
(90, '南岸区', '南岸区', 5,'500108', FALSE),
(91, '九龙坡区', '九龙坡区', 5,'500107', FALSE),
(92, '北碚区', '北碚区', 5,'500109', FALSE),
(93, '綦江区', '綦江区', 5,'500110', FALSE),
(94, '大足区', '大足区', 5,'500111', FALSE),
(95, '渝北区', '渝北区', 5,'500112', FALSE),
(96, '巴南区', '巴南区', 5,'500113', FALSE),
(97, '黔江区', '黔江区', 5,'500114', FALSE),
(98, '长寿区', '长寿区', 5,'500115', FALSE),
(99, '江津区', '江津区', 5,'500116', FALSE),
(100, '合川区', '合川区', 5,'500117', FALSE),
(101, '永川区', '永川区', 5,'500118', FALSE),
(102, '南川区', '南川区', 5,'500119', FALSE),
(103, '璧山区', '璧山区', 5,'500120', FALSE),
(104, '铜梁区', '铜梁区', 5,'500151', FALSE),
(105, '潼南区', '潼南区', 5,'500152', FALSE),
(106, '荣昌区', '荣昌区', 5,'500153', FALSE),
(107, '开州区', '开州区', 5,'500154', FALSE),
(108, '梁平区', '梁平区', 5,'500155', FALSE),
(109, '武隆区', '武隆区', 5,'500156', FALSE),
(110, '城口县', '城口县', 5,'500229', FALSE),
(111, '丰都县', '丰都县', 5,'500230', FALSE),
(112, '垫江县', '垫江县', 5,'500231', FALSE),
(113, '忠县', '忠县', 5,'500233', FALSE),
(114, '云阳县', '云阳县', 5,'500235', FALSE),
(115, '奉节县', '奉节县', 5,'500236', FALSE),
(116, '巫山县', '巫山县', 5,'500237', FALSE),
(117, '巫溪县', '巫溪县', 5,'500238', FALSE),
(118, '石柱土家族自治县', '石柱土家族自治县', 5,'500240', FALSE),
(119, '秀山土家族苗族自治县', '秀山土家族苗族自治县', 5,'500241', FALSE),
(120, '酉阳土家族苗族自治县', '酉阳土家族苗族自治县', 5,'500242', FALSE),
(121, '彭水苗族土家族自治县', '彭水苗族土家族自治县', 5,'500243', FALSE);
-- 河北省
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(122, 'sjz', '石家庄市', 6, '', FALSE),
(123, 'tangshan', '唐山市', 6, '', FALSE),
(124, 'qhd', '秦皇岛市', 6, '', FALSE),
(125, 'handan', '邯郸市', 6, '', FALSE),
(126, 'xingtai', '邢台市', 6, '', FALSE),
(127, 'baoding', '保定市', 6, '', FALSE),
(128, 'zjk', '张家口市', 6, '', FALSE),
(129, 'chengde', '承德市', 6, '', FALSE),
(130, 'cangzhou', '沧州市', 6, '', FALSE),
(131, 'langfang', '廊坊市', 6, '', FALSE),
(132, 'hengshui', '衡水市', 6, '', FALSE);
-- 山西省
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(133, 'taiyuan', '太原市', 7, '', FALSE),
(134, 'datong', '大同市', 7, '', FALSE),
(135, 'yangquan', '阳泉市', 7, '', FALSE),
(136, 'zhangzhi', '长治市', 7, '', FALSE),
(137, 'jincheng', '晋城市', 7, '', FALSE),
(138, 'shuozhou', '朔州市', 7, '', FALSE),
(139, 'jinzhong', '晋中市', 7, '', FALSE),
(140, 'yuncheng', '运城市', 7, '', FALSE),
(141, 'xinzhou', '忻州市', 7, '', FALSE),
(142, 'linfen', '临汾市', 7, '', FALSE),
(143, 'lvliang', '吕梁市', 7, '', FALSE);
-- 内蒙古自治区
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(144, 'hhht', '呼和浩特市', 8, '', FALSE),
(145, 'baotou', '包头市', 8, '', FALSE),
(146, 'wuhai', '乌海市', 8, '', FALSE),
(147, 'chifeng', '赤峰市', 8, '', FALSE),
(148, 'tongliao', '通辽市', 8, '', FALSE),
(149, 'eeds', '鄂尔多斯市', 8, '', FALSE),
(150, 'hlbe', '呼伦贝尔市', 8, '', FALSE),
(151, 'byne', '巴彦淖尔市', 8, '', FALSE),
(152, 'wlcb', '乌兰察布市', 8, '', FALSE),
(153, 'xam', '兴安盟', 8, '', FALSE),
(154, 'xlglm', '锡林郭勒盟', 8, '', FALSE),
(155, 'alsm', '阿拉善盟', 8, '', FALSE);
-- 辽宁省
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(156, 'shenyang', '沈阳市', 9, '', FALSE),
(157, 'dalian', '大连市', 9, '', FALSE),
(158, 'anshan', '鞍山市', 9, '', FALSE),
(159, 'fushun', '抚顺市', 9, '', FALSE),
(160, 'benxi', '本溪市', 9, '', FALSE),
(161, 'dandong', '丹东市', 9, '', FALSE),
(162, 'jinzhou', '锦州市', 9, '', FALSE),
(163, 'fuxin', '阜新市', 9, '', FALSE),
(164, 'liaoyang', '辽阳市', 9, '', FALSE),
(165, 'panjin', '盘锦市', 9, '', FALSE),
(166, 'tieling', '铁岭市', 9, '', FALSE),
(167, 'chaoyang', '朝阳市', 9, '', FALSE),
(168, 'hld', '葫芦岛市', 9, '', FALSE);
-- 吉林省
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(169, 'zhangchun', '长春市', 10, '', FALSE),
(170, 'jilin', '吉林市', 10, '', FALSE),
(171, 'siping', '四平市', 10, '', FALSE),
(172, 'liaoyuan', '辽源市', 10, '', FALSE),
(173, 'tonghua', '通化市', 10, '', FALSE),
(174, 'baishan', '白山市', 10, '', FALSE),
(175, 'songyuan', '松原市', 10, '', FALSE),
(176, 'baicheng', '白城市', 10, '', FALSE),
(177, 'ybcxz', '延边朝鲜族自治州', 10, '', FALSE);
-- 黑龙江省
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(178, 'herb', '哈尔滨市', 11, '', FALSE),
(179, 'qqhe', '齐齐哈尔市', 11, '', FALSE),
(180, 'jixi', '鸡西市', 11, '', FALSE),
(181, 'hegang', '鹤岗市', 11, '', FALSE),
(182, 'sys', '双鸭山市', 11, '', FALSE),
(183, 'daqing', '大庆市', 11, '', FALSE),
(184, 'yich', '伊春市', 11, '', FALSE),
(185, 'jms', '佳木斯市', 11, '', FALSE),
(186, 'qth', '七台河市', 11, '', FALSE),
(187, 'mdj', '牡丹江市', 11, '', FALSE),
(188, 'heihe', '黑河市', 11, '', FALSE),
(189, 'suihua', '绥化市', 11, '', FALSE),
(190, 'dxaldq', '大兴安岭地区', 11, '', FALSE);
-- 江苏省
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(191, 'nanjing', '南京市', 12, '', FALSE),
(192, 'wuxi', '无锡市', 12, '', FALSE),
(193, 'xuzhou', '徐州市', 12, '', FALSE),
(194, 'changzhou', '常州市', 12, '', FALSE),
(195, 'szh', '苏州市', 12, '', FALSE),
(196, 'nantong', '南通市', 12, '', FALSE),
(197, 'lyg', '连云港市', 12, '', FALSE),
(198, 'huaian', '淮安市', 12, '', FALSE),
(199, 'yancheng', '盐城市', 12, '', FALSE),
(200, 'yangzhou', '扬州市', 12, '', FALSE),
(201, 'zhenjiang', '镇江市', 12, '', FALSE),
(202, 'tzh', '泰州市', 12, '', FALSE),
(203, 'suqian', '宿迁市', 12, '', FALSE);
-- 安徽省
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(204, 'hefei', '合肥市', 14, '', FALSE),
(205, 'wuhu', '芜湖市', 14, '', FALSE),
(206, 'bangbu', '蚌埠市', 14, '', FALSE),
(207, 'huainan', '淮南市', 14, '', FALSE),
(208, 'mas', '马鞍山市', 14, '', FALSE),
(209, 'huaibei', '淮北市', 14, '', FALSE),
(210, 'tongling', '铜陵市', 14, '', FALSE),
(211, 'anqing', '安庆市', 14, '', FALSE),
(212, 'huangshan', '黄山市', 14, '', FALSE),
(213, 'chuzhou', '滁州市', 14, '', FALSE),
(214, 'fuyang', '阜阳市', 14, '', FALSE),
(215, 'suzhou', '宿州市', 14, '', FALSE),
(216, 'liuan', '六安市', 14, '', FALSE),
(217, 'bozhou', '亳州市', 14, '', FALSE),
(218, 'chizhou', '池州市', 14, '', FALSE),
(219, 'xuancheng', '宣城市', 14, '', FALSE);
-- 浙江省
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(220, 'hangzhou', '杭州市', 13, '', FALSE),
(221, 'ningbo', '宁波市', 13, '', FALSE),
(222, 'wenzhou', '温州市', 13, '', FALSE),
(223, 'jiaxing', '嘉兴市', 13, '', FALSE),
(224, 'huzhou', '湖州市', 13, '', FALSE),
(225, 'shaoxing', '绍兴市', 13, '', FALSE),
(226, 'jinhua', '金华市', 13, '', FALSE),
(227, 'quzhou', '衢州市', 13, '', FALSE),
(228, 'zhoushan', '舟山市', 13, '', FALSE),
(229, 'taizhou', '台州市', 13, '', FALSE),
(230, 'lishui', '丽水市', 13, '', FALSE);
-- 福建省
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(231, 'fzh', '福州市', 15, '', FALSE),
(232, 'shamen', '厦门市', 15, '', FALSE),
(233, 'putian', '莆田市', 15, '', FALSE),
(234, 'sanming', '三明市', 15, '', FALSE),
(235, 'quanzhou', '泉州市', 15, '', FALSE),
(236, 'zhangzhou', '漳州市', 15, '', FALSE),
(237, 'nanping', '南平市', 15, '', FALSE),
(238, 'longyan', '龙岩市', 15, '', FALSE),
(239, 'ningde', '宁德市', 15, '', FALSE);
-- 江西省
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(240, 'nanchang', '南昌市', 16, '', FALSE),
(241, 'jdz', '景德镇市', 16, '', FALSE),
(243, 'pingxiang', '萍乡市', 16, '', FALSE),
(244, 'jiujiang', '九江市', 16, '', FALSE),
(245, 'xinyu', '新余市', 16, '', FALSE),
(246, 'yingtan', '鹰潭市', 16, '', FALSE),
(247, 'ganzhou', '赣州市', 16, '', FALSE),
(248, 'jian', '吉安市', 16, '', FALSE),
(249, 'ych', '宜春市', 16, '', FALSE),
(250, 'fuzhou', '抚州市', 16, '', FALSE),
(251, 'shangrao', '上饶市', 16, '', FALSE);
-- 山东省
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(252, 'jinan', '济南市', 17, '', FALSE),
(253, 'qingdao', '青岛市', 17, '', FALSE),
(254, 'zibo', '淄博市', 17, '', FALSE),
(255, 'zaozhuang', '枣庄市', 17, '', FALSE),
(256, 'dongying', '东营市', 17, '', FALSE),
(257, 'yantai', '烟台市', 17, '', FALSE),
(258, 'weifang', '潍坊市', 17, '', FALSE),
(259, 'jining', '济宁市', 17, '', FALSE),
(260, 'taian', '泰安市', 17, '', FALSE),
(261, 'weihai', '威海市', 17, '', FALSE),
(262, 'rizhao', '日照市', 17, '', FALSE),
(263, 'laiwu', '莱芜市', 17, '', FALSE),
(264, 'linyi', '临沂市', 17, '', FALSE),
(265, 'dezhou', '德州市', 17, '', FALSE),
(266, 'liaocheng', '聊城市', 17, '', FALSE),
(267, 'binzhou', '滨州市', 17, '', FALSE),
(268, 'heze', '菏泽市', 17, '', FALSE);
-- 河南省
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(269, 'zhengzhou', '郑州市', 18, '', FALSE),
(270, 'kaifeng', '开封市', 18, '', FALSE),
(271, 'luoyang', '洛阳市', 18, '', FALSE),
(272, 'pds', '平顶山市', 18, '', FALSE),
(273, 'anyang', '安阳市', 18, '', FALSE),
(274, 'hebi', '鹤壁市', 18, '', FALSE),
(275, 'xinxiang', '新乡市', 18, '', FALSE),
(276, 'puyang', '濮阳市', 18, '', FALSE),
(277, 'xuchang', '许昌市', 18, '', FALSE),
(278, 'luohe', '漯河市', 18, '', FALSE),
(279, 'smx', '三门峡市', 18, '', FALSE),
(280, 'nanyang', '南阳市', 18, '', FALSE),
(281, 'shangqiu', '商丘市', 18, '', FALSE),
(282, 'xinyang', '信阳市', 18, '', FALSE),
(283, 'zhoukou', '周口市', 18, '', FALSE),
(284, 'zmd', '驻马店市', 18, '', FALSE),
(285, 'henzx', '省直辖县级行政区划', 18, '', FALSE);
-- 湖北省
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(286, 'wuhan', '武汉市', 19, '', FALSE),
(287, 'huangshi', '黄石市', 19, '', FALSE),
(288, 'shiyan', '十堰市', 19, '', FALSE),
(289, 'yichang', '宜昌市', 19, '', FALSE),
(290, 'xiangyang', '襄阳市', 19, '', FALSE),
(291, 'ezhou', '鄂州市', 19, '', FALSE),
(292, 'jingmen', '荆门市', 19, '', FALSE),
(293, 'xiaogan', '孝感市', 19, '', FALSE),
(294, 'jingzhou', '荆州市', 19, '', FALSE),
(295, 'huanggang', '黄冈市', 19, '', FALSE),
(296, 'xianning', '咸宁市', 19, '', FALSE),
(297, 'suizhou', '随州市', 19, '', FALSE),
(298, 'estjz', '恩施土家族苗族自治州', 19, '', FALSE),
(299, 'hubzx', '省直辖县级行政区划', 19, '', FALSE);
-- 湖南省
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(300, 'zhangsha', '长沙市', 20, '', FALSE),
(301, 'zhuzhou', '株洲市', 20, '', FALSE),
(302, 'xiangtan', '湘潭市', 20, '', FALSE),
(303, 'hengyang', '衡阳市', 20, '', FALSE),
(304, 'shaoyang', '邵阳市', 20, '', FALSE),
(305, 'yueyang', '岳阳市', 20, '', FALSE),
(306, 'changde', '常德市', 20, '', FALSE),
(307, 'zjj', '张家界市', 20, '', FALSE),
(308, 'yiyang', '益阳市', 20, '', FALSE),
(309, 'chenzhou', '郴州市', 20, '', FALSE),
(310, 'yongzhou', '永州市', 20, '', FALSE),
(311, 'huaihua', '怀化市', 20, '', FALSE),
(312, 'loudi', '娄底市', 20, '', FALSE);
-- 广东省
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(313, 'guangzhou', '广州市', 21, '', FALSE),
(314, 'shaoguan', '韶关市', 21, '', FALSE),
(315, 'shenzhen', '深圳市', 21, '', FALSE),
(316, 'zhuhai', '珠海市', 21, '', FALSE),
(317, 'shantou', '汕头市', 21, '', FALSE),
(318, 'foshan', '佛山市', 21, '', FALSE),
(319, 'jiangmen', '江门市', 21, '', FALSE),
(320, 'zhanjiang', '湛江市', 21, '', FALSE),
(321, 'maoming', '茂名市', 21, '', FALSE),
(322, 'zhaoqing', '肇庆市', 21, '', FALSE),
(323, 'huizhou', '惠州市', 21, '', FALSE),
(324, 'meizhou', '梅州市', 21, '', FALSE),
(325, 'shanwei', '汕尾市', 21, '', FALSE),
(326, 'heyuan', '河源市', 21, '', FALSE),
(327, 'yangjiang', '阳江市', 21, '', FALSE),
(328, 'qingyuan', '清远市', 21, '', FALSE),
(329, 'dongguan', '东莞市', 21, '', FALSE),
(330, 'chaozhou', '潮州市', 21, '', FALSE),
(331, 'zhongshan', '中山市', 21, '', FALSE),
(332, 'jieyang', '揭阳市', 21, '', FALSE),
(333, 'yunfu', '云浮市', 21, '', FALSE);
-- 广西壮族自治区
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(334, 'nanning', '南宁市', 22, '', FALSE),
(335, 'liuzhou', '柳州市', 22, '', FALSE),
(336, 'guilin', '桂林市', 22, '', FALSE),
(337, 'wuzhou', '梧州市', 22, '', FALSE),
(338, 'beihai', '北海市', 22, '', FALSE),
(339, 'fcg', '防城港市', 22, '', FALSE),
(340, 'qinzhou', '钦州市', 22, '', FALSE),
(341, 'guigang', '贵港市', 22, '', FALSE),
(342, 'yul', '玉林市', 22, '', FALSE),
(343, 'baise', '百色市', 22, '', FALSE),
(344, 'hezhou', '贺州市', 22, '', FALSE),
(345, 'hechi', '河池市', 22, '', FALSE),
(346, 'laibin', '来宾市', 22, '', FALSE),
(347, 'chongzuo', '崇左市', 22, '', FALSE);
-- 四川省
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(348, 'chengdu', '成都市', 23, '', FALSE),
(349, 'zigong', '自贡市', 23, '', FALSE),
(350, 'pzh', '攀枝花市', 23, '', FALSE),
(351, 'luzhou', '泸州市', 23, '', FALSE),
(352, 'dezhou', '德州市', 23, '', FALSE),
(353, 'mianyang', '绵阳市', 23, '', FALSE),
(354, 'guangyuan', '广元市', 23, '', FALSE),
(355, 'suining', '遂宁市', 23, '', FALSE),
(356, 'neijiang', '内江市', 23, '', FALSE),
(357, 'leshan', '乐山市', 23, '', FALSE),
(358, 'nanchong', '南充市', 23, '', FALSE),
(359, 'meishan', '眉山市', 23, '', FALSE),
(360, 'yibin', '宜宾市', 23, '', FALSE),
(361, 'guagan', '广安市', 23, '', FALSE),
(362, 'dazhou', '达州市', 23, '', FALSE),
(363, 'yaan', '雅安市', 23, '', FALSE),
(364, 'bazhong', '巴中市', 23, '', FALSE),
(365, 'ziyanh', '资阳市', 23, '', FALSE),
(366, 'abzzqz', '阿坝藏族羌族自治州', 23, '', FALSE),
(367, 'gzzz', '甘孜藏族自治州', 23, '', FALSE),
(368, 'lsyz', '凉山彝族自治州', 23, '', FALSE);
-- 贵州省
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(369, 'guiyang', '贵阳市', 24, '', FALSE),
(370, 'lps', '六盘水市', 24, '', FALSE),
(371, 'zunyi', '遵义市', 24, '', FALSE),
(372, 'anshun', '安顺市', 24, '', FALSE),
(373, 'bijie', '毕节市', 24, '', FALSE),
(374, 'tongren', '铜仁市', 24, '', FALSE),
(375, 'qxnbyz', '黔西南布依族苗族自治州', 24, '', FALSE),
(376, 'qdnz', '黔东南苗族侗族自治州', 24, '', FALSE),
(377, 'qnbyz', '黔南布依族苗族自治州', 24, '', FALSE);
-- 云南省
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(378, 'kunming', '昆明市', 25, '', FALSE),
(379, 'qujing', '曲靖市', 25, '', FALSE),
(380, 'yuxi', '玉溪市', 25, '', FALSE),
(381, 'baoshan', '保山市', 25, '', FALSE),
(382, 'zhaotong', '昭通市', 25, '', FALSE),
(383, 'lijiang', '丽江市', 25, '', FALSE),
(384, 'puer', '普洱市', 25, '', FALSE),
(385, 'lincang', '临沧市', 25, '', FALSE),
(386, 'cxyz', '楚雄彝族自治州', 25, '', FALSE),
(387, 'hhhnzyz', '红河哈尼族彝族自治州', 25, '', FALSE),
(388, 'wszzmz', '文山壮族苗族自治州', 25, '', FALSE),
(389, 'xsbndz', '西双版纳傣族自治州', 25, '', FALSE),
(390, 'dlbz', '大理白族自治州', 25, '', FALSE),
(391, 'dhdzjpz', '德宏傣族景颇族自治州', 25, '', FALSE),
(392, 'njlsz', '怒江傈僳族自治州', 25, '', FALSE),
(393, 'dqzz', '迪庆藏族自治州', 25, '', FALSE);
-- 海南省
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(394, 'haikou', '海口市', 26, '', FALSE),
(395, 'sanya', '三亚市', 26, '', FALSE),
(396, 'sansha', '三沙市', 26, '', FALSE),
(397, 'hanzx', '省直辖县级行政区划', 26, '', FALSE);
-- 陕西省
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(398, 'xian', '西安市', 27, '', FALSE),
(399, 'tongchuan', '铜川市', 27, '', FALSE),
(400, 'baoji', '宝鸡市', 27, '', FALSE),
(401, 'xianyang', '咸阳市', 27, '', FALSE),
(402, 'weinan', '渭南市', 27, '', FALSE),
(403, 'yanan', '延安市', 27, '', FALSE),
(404, 'hanzhong', '汉中市', 27, '', FALSE),
(405, 'yulin', '榆林市', 27, '', FALSE),
(406, 'ankang', '安康市', 27, '', FALSE),
(407, 'shangqiu', '商丘市', 27, '', FALSE);
-- 甘肃省
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(408, 'lanzhou', '兰州市', 28, '', FALSE),
(409, 'jinchang', '金昌市', 28, '', FALSE),
(410, 'baiyin', '白银市', 28, '', FALSE),
(411, 'tianshui', '天水市', 28, '', FALSE),
(412, 'wuwei', '武威市', 28, '', FALSE),
(413, 'zhangye', '张掖市', 28, '', FALSE),
(414, 'pingliang', '平凉市', 28, '', FALSE),
(415, 'jiuquan', '酒泉市', 28, '', FALSE),
(416, 'qingyang', '庆阳市', 28, '', FALSE),
(417, 'dingxi', '定西市', 28, '', FALSE),
(418, 'longnan', '陇南市', 28, '', FALSE),
(419, 'lxhz', '临夏回族自治州', 28, '', FALSE),
(420, 'jyg', '嘉峪关市', 28, '', FALSE),
(421, 'gnzz', '甘南藏族自治州', 28, '', FALSE);
-- 宁夏回族自治区
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(422, 'yinchuan', '银川市', 29, '', FALSE),
(423, 'szs', '石嘴山市', 29, '', FALSE),
(424, 'wuzhong', '吴忠市', 29, '', FALSE),
(425, 'guyuan', '固原市', 29, '', FALSE),
(426, 'zhongwei', '中卫市', 29, '', FALSE);
-- 青海省
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(427, 'xining', '西宁市', 30, '', FALSE),
(428, 'haidong', '海东市', 30, '', FALSE),
(429, 'hbzz', '海北藏族自治州', 30, '', FALSE),
(430, 'hunzz', '黄南藏族自治州', 30, '', FALSE),
(431, 'hnzz', '海南藏族自治州', 30, '', FALSE),
(432, 'glzz', '果洛藏族自治州', 30, '', FALSE),
(433, 'yszz', '玉树藏族自治州', 30, '', FALSE),
(434, 'hxmgz', '海西蒙古族藏族自治州', 30, '', FALSE);
-- 新疆维吾尔自治区
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(435, 'wlmq', '乌鲁木齐市', 31, '', FALSE),
(436, 'klmy', '克拉玛依市', 31, '', FALSE),
(437, 'tlfdq', '吐鲁番市', 31, '', FALSE),
(438, 'hmdq', '哈密市', 31, '', FALSE),
(439, 'cjhz', '昌吉回族自治州', 31, '', FALSE),
(440, 'betlmg', '博尔塔拉蒙古自治州', 31, '', FALSE),
(441, 'byglmg', '巴音郭楞蒙古自治州', 31, '', FALSE),
(442, 'aksdq', '阿克苏地区', 31, '', FALSE),
(443, 'kzlskek', '克孜勒苏柯尔克孜自治州', 31, '', FALSE),
(444, 'ksdq', '喀什地区', 31, '', FALSE),
(445, 'htdq', '和田地区', 31, '', FALSE),
(446, 'ylhsk', '伊犁哈萨克自治州', 31, '', FALSE),
(447, 'tcdq', '塔城地区', 31, '', FALSE),
(448, 'altdq', '阿勒泰地区', 31, '', FALSE),
(449, 'xjzx', '自治区直辖县级行政区划', 31, '', FALSE);
-- 西藏自治区
INSERT INTO citys(id, name, full_name, parent_id, code, is_cg) VALUES
(450, 'lasa', '拉萨市', 32, '', FALSE),
(451, 'rkz', '日喀则市', 32, '', FALSE),
(452, 'cddq', '昌都市', 32, '', FALSE),
(453, 'lzdq', '林芝市', 32, '', FALSE),
(454, 'sndq', '山南市', 32, '', FALSE),
(455, 'aldq', '阿里地区', 32, '', FALSE),
(456, 'nqdq', '那曲市', 32, '', FALSE);




