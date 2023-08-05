在对象存储中, 按<代理产品资源交付规则>创建目录及制定交付包名称

s3-obj-semver 首先按semver规则, 取得最大版本号; 然后以版本编译(构建)信息中的最后一位(以.分隔)排序. 获取到最大版本号, 且是最大构建号, 并以key=value的形式输出

代码仓库

  https://code.ppgame.com/JenkinsABS/tool-S3ObjVersion

可用客户端:

  AWS s3

  Tencent COS

  Minio

输出

  S3PKG_VERSION=1.0.3+15047.0004
