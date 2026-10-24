# PT-15.3.3 — Aplicacao Colmeia Embarcada / Needle 2
# Destino: firmware/esp32/colmeia_needle/main/CMakeLists.txt

set(ND_SCHEMA_PATH "${CMAKE_CURRENT_LIST_DIR}/../../../tools/colmeia.json")

file(READ "${ND_SCHEMA_PATH}" ND_SCHEMA_RAW)
string(REGEX REPLACE "[\r\n]" "" ND_SCHEMA_RAW "${ND_SCHEMA_RAW}")
string(STRIP "${ND_SCHEMA_RAW}" ND_SCHEMA_RAW)
string(REPLACE "\\" "\\\\" ND_SCHEMA_ESC "${ND_SCHEMA_RAW}")
string(REPLACE "\"" "\\\"" ND_SCHEMA_ESC "${ND_SCHEMA_ESC}")

configure_file(
    "${CMAKE_CURRENT_LIST_DIR}/tools_schema.h.in"
    "${CMAKE_CURRENT_BINARY_DIR}/generated/tools_schema.h"
    @ONLY
)

set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS "${ND_SCHEMA_PATH}")

idf_component_register(
    SRCS "main.c" "colmeia_tools.c"
    INCLUDE_DIRS "." "${CMAKE_CURRENT_BINARY_DIR}/generated"
    REQUIRES needle esp_driver_rmt esp_driver_gpio esp_partition esp_timer
)
