[app]

title = StarVowPoem
package.name = starvowpoem
package.domain = org.starvowpoem

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,json
source.main = mobile_app.py

version = 1.0.0

requirements = python3,kivy

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.archs = arm64-v8a,armeabi-v7a

android.api = 31
android.minapi = 21
android.ndk = 25b

orientation = portrait
fullscreen = 0

[buildozer]

log_level = 2
warn_on_root = 1
