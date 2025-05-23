cmake_minimum_required(VERSION 3.16)
project(AscendOS)

set(CMAKE_CXX_STANDARD 17)

# Tell CMake where Qt6 is (if you installed via brew)
set(CMAKE_PREFIX_PATH "/usr/local/opt/qt")

# Find Qt6
find_package(Qt6 REQUIRED COMPONENTS Widgets)

# Include necessary modules
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)

# Add sources
set(SOURCES
    main.cpp
    mainwindow.cpp
)

set(HEADERS
    mainwindow.h
)

set(UIS
    mainwindow.ui
)

# Create executable
add_executable(AscendOS ${SOURCES} ${HEADERS} ${UIS})

# Link Qt6
target_link_libraries(AscendOS PRIVATE Qt6::Widgets)
