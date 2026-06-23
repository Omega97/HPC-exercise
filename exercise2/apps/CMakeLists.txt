find_package(OpenMP REQUIRED)

set(EXECUTABLE_NAME mandelbrot)
set(SOURCE_FILES main.c)

set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)

set(INCLUDE_DIRS
    ${CMAKE_SOURCE_DIR}/include
)

include_directories(${INCLUDE_DIRS})

add_executable(${EXECUTABLE_NAME} ${SOURCE_FILES})

target_link_libraries(${EXECUTABLE_NAME} PRIVATE OpenMP::OpenMP_C mandelbrot_lib)