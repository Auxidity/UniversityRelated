cmake_minimum_required(VERSION 3.16)
project(hello VERSION 0.1.0 LANGUAGES C CXX)

add_executable(lab4.2 main.c timers_init.c)
target_link_libraries(lab4.2 /var/lib/schroot/chroots/rpi3-bookworm-armhf/usr/lib/arm-linux-gnueabihf/librt.so)
target_link_libraries(lab4.2 /var/lib/schroot/chroots/rpi3-bookworm-armhf/usr/lib/arm-linux-gnueabihf/libgpiod.so)
include_directories(/var/lib/schroot/chroots/rpi3-bookworm-armhf/usr/local/include/) 
include_directories(/var/lib/schroot/chroots/rpi3-bookworm-armhf/usr/include/) 
include_directories(/var/lib/schroot/chroots/rpi3-bookworm-armhf/usr/include/arm-linux-gnueabihf/) 



add_custom_target(copy_wrapper_script ALL
COMMAND ${CMAKE_COMMAND} -E copy
        ${CMAKE_SOURCE_DIR}/table.txt
        ${CMAKE_CURRENT_BINARY_DIR}/table.txt
COMMENT "Copying table.txt to build directory"
VERBATIM
)

add_custom_command(TARGET lab4.2
    POST_BUILD
    COMMAND ssh pi@auxi.local "rm -f /home/pi/table.txt"
    COMMAND scp ${CMAKE_SOURCE_DIR}/table.txt pi@auxi.local:/home/pi
    #COMMAND ssh pi@auxi.local "chmod +x /home/pi/table.txt"
    COMMENT "Copying and setting permissions for table.txt on Raspberry Pi"
    VERBATIM
)





install(TARGETS lab4.2
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
