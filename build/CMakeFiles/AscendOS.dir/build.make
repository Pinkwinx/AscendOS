# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 4.0

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/bin/cmake

# The command to remove a file.
RM = /usr/local/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/marianguyen/Documents/GitHub/AscendOS

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/marianguyen/Documents/GitHub/AscendOS/build

# Include any dependencies generated for this target.
include CMakeFiles/AscendOS.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/AscendOS.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/AscendOS.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/AscendOS.dir/flags.make

AscendOS_autogen/timestamp: /usr/local/opt/qt/share/qt/libexec/moc
AscendOS_autogen/timestamp: /usr/local/opt/qt/share/qt/libexec/uic
AscendOS_autogen/timestamp: CMakeFiles/AscendOS.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --blue --bold --progress-dir=/Users/marianguyen/Documents/GitHub/AscendOS/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Automatic MOC and UIC for target AscendOS"
	/usr/local/bin/cmake -E cmake_autogen /Users/marianguyen/Documents/GitHub/AscendOS/build/CMakeFiles/AscendOS_autogen.dir/AutogenInfo.json ""
	/usr/local/bin/cmake -E touch /Users/marianguyen/Documents/GitHub/AscendOS/build/AscendOS_autogen/timestamp

CMakeFiles/AscendOS.dir/codegen:
.PHONY : CMakeFiles/AscendOS.dir/codegen

CMakeFiles/AscendOS.dir/AscendOS_autogen/mocs_compilation.cpp.o: CMakeFiles/AscendOS.dir/flags.make
CMakeFiles/AscendOS.dir/AscendOS_autogen/mocs_compilation.cpp.o: AscendOS_autogen/mocs_compilation.cpp
CMakeFiles/AscendOS.dir/AscendOS_autogen/mocs_compilation.cpp.o: CMakeFiles/AscendOS.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/Users/marianguyen/Documents/GitHub/AscendOS/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/AscendOS.dir/AscendOS_autogen/mocs_compilation.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/AscendOS.dir/AscendOS_autogen/mocs_compilation.cpp.o -MF CMakeFiles/AscendOS.dir/AscendOS_autogen/mocs_compilation.cpp.o.d -o CMakeFiles/AscendOS.dir/AscendOS_autogen/mocs_compilation.cpp.o -c /Users/marianguyen/Documents/GitHub/AscendOS/build/AscendOS_autogen/mocs_compilation.cpp

CMakeFiles/AscendOS.dir/AscendOS_autogen/mocs_compilation.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/AscendOS.dir/AscendOS_autogen/mocs_compilation.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/marianguyen/Documents/GitHub/AscendOS/build/AscendOS_autogen/mocs_compilation.cpp > CMakeFiles/AscendOS.dir/AscendOS_autogen/mocs_compilation.cpp.i

CMakeFiles/AscendOS.dir/AscendOS_autogen/mocs_compilation.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/AscendOS.dir/AscendOS_autogen/mocs_compilation.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/marianguyen/Documents/GitHub/AscendOS/build/AscendOS_autogen/mocs_compilation.cpp -o CMakeFiles/AscendOS.dir/AscendOS_autogen/mocs_compilation.cpp.s

CMakeFiles/AscendOS.dir/main.cpp.o: CMakeFiles/AscendOS.dir/flags.make
CMakeFiles/AscendOS.dir/main.cpp.o: /Users/marianguyen/Documents/GitHub/AscendOS/main.cpp
CMakeFiles/AscendOS.dir/main.cpp.o: CMakeFiles/AscendOS.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/Users/marianguyen/Documents/GitHub/AscendOS/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object CMakeFiles/AscendOS.dir/main.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/AscendOS.dir/main.cpp.o -MF CMakeFiles/AscendOS.dir/main.cpp.o.d -o CMakeFiles/AscendOS.dir/main.cpp.o -c /Users/marianguyen/Documents/GitHub/AscendOS/main.cpp

CMakeFiles/AscendOS.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/AscendOS.dir/main.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/marianguyen/Documents/GitHub/AscendOS/main.cpp > CMakeFiles/AscendOS.dir/main.cpp.i

CMakeFiles/AscendOS.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/AscendOS.dir/main.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/marianguyen/Documents/GitHub/AscendOS/main.cpp -o CMakeFiles/AscendOS.dir/main.cpp.s

CMakeFiles/AscendOS.dir/mainwindow.cpp.o: CMakeFiles/AscendOS.dir/flags.make
CMakeFiles/AscendOS.dir/mainwindow.cpp.o: /Users/marianguyen/Documents/GitHub/AscendOS/mainwindow.cpp
CMakeFiles/AscendOS.dir/mainwindow.cpp.o: CMakeFiles/AscendOS.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/Users/marianguyen/Documents/GitHub/AscendOS/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building CXX object CMakeFiles/AscendOS.dir/mainwindow.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/AscendOS.dir/mainwindow.cpp.o -MF CMakeFiles/AscendOS.dir/mainwindow.cpp.o.d -o CMakeFiles/AscendOS.dir/mainwindow.cpp.o -c /Users/marianguyen/Documents/GitHub/AscendOS/mainwindow.cpp

CMakeFiles/AscendOS.dir/mainwindow.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/AscendOS.dir/mainwindow.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/marianguyen/Documents/GitHub/AscendOS/mainwindow.cpp > CMakeFiles/AscendOS.dir/mainwindow.cpp.i

CMakeFiles/AscendOS.dir/mainwindow.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/AscendOS.dir/mainwindow.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/marianguyen/Documents/GitHub/AscendOS/mainwindow.cpp -o CMakeFiles/AscendOS.dir/mainwindow.cpp.s

# Object files for target AscendOS
AscendOS_OBJECTS = \
"CMakeFiles/AscendOS.dir/AscendOS_autogen/mocs_compilation.cpp.o" \
"CMakeFiles/AscendOS.dir/main.cpp.o" \
"CMakeFiles/AscendOS.dir/mainwindow.cpp.o"

# External object files for target AscendOS
AscendOS_EXTERNAL_OBJECTS =

AscendOS: CMakeFiles/AscendOS.dir/AscendOS_autogen/mocs_compilation.cpp.o
AscendOS: CMakeFiles/AscendOS.dir/main.cpp.o
AscendOS: CMakeFiles/AscendOS.dir/mainwindow.cpp.o
AscendOS: CMakeFiles/AscendOS.dir/build.make
AscendOS: /usr/local/opt/qt/lib/QtWidgets.framework/Versions/A/QtWidgets
AscendOS: /usr/local/opt/qt/lib/QtGui.framework/Versions/A/QtGui
AscendOS: /usr/local/opt/qt/lib/QtCore.framework/Versions/A/QtCore
AscendOS: CMakeFiles/AscendOS.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --bold --progress-dir=/Users/marianguyen/Documents/GitHub/AscendOS/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Linking CXX executable AscendOS"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/AscendOS.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/AscendOS.dir/build: AscendOS
.PHONY : CMakeFiles/AscendOS.dir/build

CMakeFiles/AscendOS.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/AscendOS.dir/cmake_clean.cmake
.PHONY : CMakeFiles/AscendOS.dir/clean

CMakeFiles/AscendOS.dir/depend: AscendOS_autogen/timestamp
	cd /Users/marianguyen/Documents/GitHub/AscendOS/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/marianguyen/Documents/GitHub/AscendOS /Users/marianguyen/Documents/GitHub/AscendOS /Users/marianguyen/Documents/GitHub/AscendOS/build /Users/marianguyen/Documents/GitHub/AscendOS/build /Users/marianguyen/Documents/GitHub/AscendOS/build/CMakeFiles/AscendOS.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : CMakeFiles/AscendOS.dir/depend

