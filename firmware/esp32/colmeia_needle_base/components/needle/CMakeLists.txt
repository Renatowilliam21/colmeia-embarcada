# PT-15.3.2 — Componente Needle 2 para Colmeia Embarcada
# Caminho: firmware/esp32/colmeia_needle/components/needle/CMakeLists.txt

set(NEEDLE_ENGINE_DIR
    "${CMAKE_CURRENT_LIST_DIR}/../../../../../external/needle-2-esp32/engine"
)

idf_component_register(
    SRCS
        "${NEEDLE_ENGINE_DIR}/src/nd_cact.c"
        "${NEEDLE_ENGINE_DIR}/src/nd_grammar.c"
        "${NEEDLE_ENGINE_DIR}/src/nd_model.c"
        "${NEEDLE_ENGINE_DIR}/src/nd_quant.c"
        "${NEEDLE_ENGINE_DIR}/src/nd_sample.c"
        "${NEEDLE_ENGINE_DIR}/src/nd_tokenizer.c"
    INCLUDE_DIRS
        "${NEEDLE_ENGINE_DIR}/include"
)
