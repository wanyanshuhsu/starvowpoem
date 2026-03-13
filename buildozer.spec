[app]

# 应用标题
title = 星誓诗笺

# 包名
package.name = starvowpoem

# 包域名
package.domain = org.starvowpoem

# 源码目录
source.dir = .

# 源码包含的文件
source.include_exts = py,png,jpg,kv,atlas,db,json

# 主程序入口
source.main = mobile_app.py

# 版本号
version = 1.0.0

# 应用需要的权限
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,CAMERA

# 支持的Android架构
android.archs = arm64-v8a,armeabi-v7a

# Python依赖
requirements = python3,kivy==2.2.1,pillow

# 应用图标（可选）
#icon.filename = %(source.dir)s/icon.png

# 启动画面（可选）
#presplash.filename = %(source.dir)s/presplash.png

# Android API版本
android.api = 31
android.minapi = 21
android.ndk = 25b

# 应用方向
orientation = portrait

# 全屏模式
fullscreen = 0

# Android应用主题
android.theme = @android:style/Theme.NoTitleBar

[buildozer]

# 日志级别
log_level = 2

# 警告级别
warn_on_root = 1
