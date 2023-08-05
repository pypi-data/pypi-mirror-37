from conans.client.generators.cmake import DepsCppCmake
from conans.model import Generator


generic_find_package_template = """
message(STATUS "Conan: Using autogenerated Find{name}.cmake")
# Global approach
SET({name}_FOUND 1)
SET({name}_INCLUDE_DIRS {deps.include_paths})
SET({name}_INCLUDES {deps.include_paths})
SET({name}_DEFINITIONS {deps.defines})
SET({name}_LIBRARIES "") # Will be filled later
SET({name}_LIBRARIES_TARGETS "") # Will be filled later, if CMake 3
SET({name}_LIBS "") # Same as {name}_LIBRARIES

mark_as_advanced({name}_FOUND {name}_INCLUDE_DIRS {name}_INCLUDES
                 {name}_DEFINITIONS {name}_LIBRARIES {name}_LIBS)


# Find the real .lib/.a and add them to {name}_LIBS and {name}_LIBRARY_LIST
SET({name}_LIBRARY_LIST {deps.libs})
SET({name}_LIB_DIRS {deps.lib_paths})
foreach(_LIBRARY_NAME ${{{name}_LIBRARY_LIST}})
    unset(CONAN_FOUND_LIBRARY CACHE)
    find_library(CONAN_FOUND_LIBRARY NAME ${{_LIBRARY_NAME}} PATHS ${{{name}_LIB_DIRS}}
                 NO_DEFAULT_PATH NO_CMAKE_FIND_ROOT_PATH)
    if(CONAN_FOUND_LIBRARY)
        list(APPEND {name}_LIBRARIES ${{CONAN_FOUND_LIBRARY}})
        if(NOT ${{CMAKE_VERSION}} VERSION_LESS "3.0")
            # Create a micro-target for each lib/a found
            set(_LIB_NAME CONAN_LIB::{name}_${{_LIBRARY_NAME}})
            if(NOT TARGET ${{_LIB_NAME}})
                # Create a micro-target for each lib/a found
                add_library(${{_LIB_NAME}} UNKNOWN IMPORTED)
                set_target_properties(${{_LIB_NAME}} PROPERTIES IMPORTED_LOCATION ${{CONAN_FOUND_LIBRARY}})
                list(APPEND {name}_LIBRARIES_TARGETS ${{_LIB_NAME}})
            else()
                message(STATUS "Skipping already existing target: ${{_LIB_NAME}}")
            endif()
        endif()
        message(STATUS "Found: ${{CONAN_FOUND_LIBRARY}}")
    else()
        message(STATUS "Library ${{_LIBRARY_NAME}} not found in package, might be system one")
        list(APPEND {name}_LIBRARIES_TARGETS ${{_LIBRARY_NAME}})
        list(APPEND {name}_LIBRARIES ${{_LIBRARY_NAME}})
    endif()
endforeach()
set({name}_LIBS ${{{name}_LIBRARIES}})

if(NOT ${{CMAKE_VERSION}} VERSION_LESS "3.0")
    # Target approach
    if(NOT TARGET {name}::{name})
        add_library({name}::{name} INTERFACE IMPORTED)
        if({name}_INCLUDE_DIRS)
          set_target_properties({name}::{name} PROPERTIES
          INTERFACE_INCLUDE_DIRECTORIES "${{{name}_INCLUDE_DIRS}}")
        endif()
        set_property(TARGET {name}::{name} PROPERTY INTERFACE_LINK_LIBRARIES ${{{name}_LIBRARIES_TARGETS}} "{deps.sharedlinkflags_list}" "{deps.exelinkflags_list}")
        set_property(TARGET {name}::{name} PROPERTY INTERFACE_COMPILE_DEFINITIONS {deps.compile_definitions})
        set_property(TARGET {name}::{name} PROPERTY INTERFACE_COMPILE_OPTIONS "{deps.cppflags_list}" "{deps.cflags_list}")
    endif()
    {find_dependencies}
endif()
"""


class CMakeFindPackageGenerator(Generator):

    @property
    def filename(self):
        pass

    @property
    def content(self):
        ret = {}
        for depname, cpp_info in self.deps_build_info.dependencies:
            ret["Find%s.cmake" % depname] = self._single_find_package(depname, cpp_info)
        return ret

    @staticmethod
    def _single_find_package(name, cpp_info):
        deps = DepsCppCmake(cpp_info)
        lines = []
        if cpp_info.public_deps:
            lines = CMakeFindPackageGenerator._transitive_lines(name, cpp_info)
        tmp = generic_find_package_template.format(name=name, deps=deps,
                                                   find_dependencies="\n".join(lines))
        return tmp

    @staticmethod
    def _transitive_lines(name, cpp_info):
        lines = ["# Library dependencies", "include(CMakeFindDependencyMacro)"]
        for dep in cpp_info.public_deps:
            def property_lines(prop):
                lib_t = "%s::%s" % (name, name)
                dep_t = "%s::%s" % (dep, dep)
                return ["get_target_property(tmp %s %s)" % (dep_t, prop),
                        "if(tmp)",
                        "  set_property(TARGET %s APPEND PROPERTY %s ${tmp})" % (lib_t, prop),
                        'endif()']

            lines.append("find_dependency(%s REQUIRED)" % dep)
            lines.extend(property_lines("INTERFACE_LINK_LIBRARIES"))
            lines.extend(property_lines("INTERFACE_COMPILE_DEFINITIONS"))
            lines.extend(property_lines("INTERFACE_INCLUDE_DIRECTORIES"))
        return lines
