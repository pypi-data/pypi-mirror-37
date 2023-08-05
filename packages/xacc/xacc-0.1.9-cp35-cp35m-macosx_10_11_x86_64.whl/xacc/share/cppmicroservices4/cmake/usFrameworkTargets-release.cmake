#----------------------------------------------------------------
# Generated CMake target import file for configuration "RELEASE".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "CppMicroServices" for configuration "RELEASE"
set_property(TARGET CppMicroServices APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(CppMicroServices PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libCppMicroServices.4.0.0.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libCppMicroServices.4.0.0.dylib"
  )

list(APPEND _IMPORT_CHECK_TARGETS CppMicroServices )
list(APPEND _IMPORT_CHECK_FILES_FOR_CppMicroServices "${_IMPORT_PREFIX}/lib/libCppMicroServices.4.0.0.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
