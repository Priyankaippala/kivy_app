[app]

# Title of your application
title = My Application

# Package name (follow reverse domain convention)
package.name = com.example.myapp

# Package domain
package.domain = org.test

# Source code directory
source.dir = .

# Source files to include
source.include_exts = py,png,jpg,kv,atlas

# Application version
version = 0.1

# Application requirements
requirements = python3,kivy==2.0.0,kivymd==0.104.1

# Supported orientations
orientation = portrait

# Supported architectures
android.archs = arm64-v8a,armeabi-v7a

# Permissions
android.permissions = INTERNET

# Allow backup
android.allow_backup = True

[buildozer]

# Log level
log_level = 2

# Warn if buildozer is run as root
warn_on_root = 1
