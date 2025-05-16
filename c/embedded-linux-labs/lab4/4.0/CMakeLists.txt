cmake_minimum_required(VERSION 3.16)
project(hello VERSION 0.1.0 LANGUAGES C CXX)


set(COMMON_SRC_FILES        
        src/common.c 
)
set(SCRIPTS        
        scripts/wrapper.sh
)        

add_library(common_lib ${COMMON_SRC_FILES})


set(LAB4_LEDON_SRC
        src/lab4-ledon.c
)

set(LAB4_LEDOFF_SRC
        src/lab4-ledoff.c
)

add_executable(lab4-ledon ${LAB4_LEDON_SRC})
target_link_libraries(lab4-ledon common_lib /var/lib/schroot/chroots/rpi3-bookworm-armhf/usr/lib/arm-linux-gnueabihf/libgpiod.so)


add_executable(lab4-ledoff ${LAB4_LEDOFF_SRC})
target_link_libraries(lab4-ledoff common_lib /var/lib/schroot/chroots/rpi3-bookworm-armhf/usr/lib/arm-linux-gnueabihf/libgpiod.so)

include_directories(
        /var/lib/schroot/chroots/rpi3-bookworm-armhf/usr/local/include/
        /var/lib/schroot/chroots/rpi3-bookworm-armhf/usr/include/
        /var/lib/schroot/chroots/rpi3-bookworm-armhf/usr/include/arm-linux-gnueabihf/
)

add_custom_target(copy_wrapper_script ALL
COMMAND ${CMAKE_COMMAND} -E copy
        ${CMAKE_SOURCE_DIR}/scripts/wrapper.sh
        ${CMAKE_CURRENT_BINARY_DIR}/wrapper.sh
COMMENT "Copying wrapper.sh to build directory"
VERBATIM
)

add_custom_command(TARGET lab4-ledon
    POST_BUILD
    COMMAND ssh pi@auxi.local "rm -f /home/pi/wrapper.sh"
    COMMAND scp ${CMAKE_SOURCE_DIR}/scripts/wrapper.sh pi@auxi.local:/home/pi
    COMMAND ssh pi@auxi.local "chmod +x /home/pi/wrapper.sh"
    COMMENT "Copying and setting permissions for wrapper.sh on Raspberry Pi"
    VERBATIM
)


install(TARGETS lab4-ledon lab4-ledoff 
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})




    

