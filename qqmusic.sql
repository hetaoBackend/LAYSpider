/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50548
Source Host           : localhost:3306
Source Database       : qqmusci

Target Server Type    : MYSQL
Target Server Version : 50548
File Encoding         : 65001

Date: 2018-12-27 14:13:39
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for ablum
-- ----------------------------
DROP TABLE IF EXISTS `album`;
CREATE TABLE `album` (
  `ID` int(64) auto_increment COMMENT '自动ID',
  `AlbID` int(32) NOT NULL COMMENT '专辑ID',
  `AlbName` varchar(255) NOT NULL COMMENT '专辑名称',
  `ProID` int(32) NOT NULL COMMENT '制作人ID',
  `ProName` varchar(255) NOT NULL COMMENT '制作人名称',
  `School` varchar(255) DEFAULT NULL COMMENT '流派',
  `Language` varchar(255) DEFAULT NULL COMMENT '语种',
  `TimePub` datetime DEFAULT NULL COMMENT '发行时间',
  `Company` varchar(255) DEFAULT NULL COMMENT '发行公司',
  `SalNum` int(32) DEFAULT NULL COMMENT '已售张数',
  `PerPrice` int(11) DEFAULT NULL COMMENT '单价',
  `Intro` mediumtext COMMENT '简介',
  `SelCom` int(32) DEFAULT NULL COMMENT '精选评论数',
  `AllCom` int(32) DEFAULT NULL COMMENT '全部评论数',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `ID` int(64) auto_increment COMMENT '自动ID',
  `ComID` varchar(100) NOT NULL COMMENT '评论ID',
  `AlbID` int(32) NOT NULL COMMENT '专辑ID',
  `FanID` varchar(100) NOT NULL COMMENT '粉丝ID',
  `ComCont` mediumtext COMMENT '粉丝评论',
  `Label` varchar(255) DEFAULT NULL COMMENT '是否精选, 1代表精选',
  `Time` datetime DEFAULT NULL COMMENT '评论时间',
  `Likes` int(32) DEFAULT NULL COMMENT '评论点赞数',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for fans
-- ----------------------------
DROP TABLE IF EXISTS `fans`;
CREATE TABLE `fans` (
  `ID` int(64) auto_increment COMMENT '自动ID',
  `FanID` varchar(100) NOT NULL COMMENT '粉丝ID',
  `AlbID` int(32) NOT NULL COMMENT '专辑ID',
  `Rank` int(32) DEFAULT NULL COMMENT '排名',
  `Label` int(10) DEFAULT NULL COMMENT '土豪榜OR铁粉榜,1代表土豪榜，2代表铁粉榜',
  `FanName` varchar(255) DEFAULT NULL COMMENT '用户昵称',
  `ContriValue` int(255) DEFAULT NULL COMMENT '贡献值',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for song
-- ----------------------------
DROP TABLE IF EXISTS `song`;
CREATE TABLE `song` (
  `ID` int(64) auto_increment COMMENT '自动ID',
  `SongID` int(32) NOT NULL COMMENT '歌曲ID',
  `AlbID` int(32) NOT NULL COMMENT '专辑ID',
  `SongName` varchar(255) NOT NULL COMMENT '歌曲名称',
  `SongDur` time DEFAULT NULL COMMENT '歌曲时长',
  `SSelCom` int(32) DEFAULT NULL COMMENT '歌曲精彩评论数量',
  `SAllCom` int(32) DEFAULT NULL COMMENT '歌曲全部评论数量',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for salenum
-- ----------------------------
DROP TABLE IF EXISTS `salenum`;
CREATE TABLE `salenum` (
  `ID` int(32) auto_increment COMMENT '自动ID',
  `AlbID` int(32) NOT NULL COMMENT '专辑ID',
  `AlbName` varchar(255) NOT NULL COMMENT '专辑名称',
  `SalNum` int(64) NOT NULL COMMENT '已售张数',
  `CreateTime` datetime NOT NULL COMMENT '下载时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
