cmake_minimum_required(VERSION 3.16)

# Project name and version
project(AscendOS LANGUAGES CXX)

# Use C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Qt6 and the required components
find_package(Qt6 REQUIRED COMPONENTS Widgets)

# Enable automatic processing of .ui and .qrc files
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# Add the executable and your source files
add_executable(${PROJECT_NAME}
    main.cpp
    mainwindow.cpp
    mainwindow.h
    mainwindow.ui
)

# Link Qt6 Widgets
target_link_libraries(${PROJECT_NAME} PRIVATE Qt6::Widgets)
