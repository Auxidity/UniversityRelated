

### File Path
Executable in VM is found in ~/Desktop/EmbeddedLinux/embedded-linux-labs/lab2/build/

Executable in Raspberry is found in ~/home/pi/

### Architecture
Architecture the executable was built for is 

lab2: ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux-armhf.so.3, for GNU/Linux 5.15.138, with debug_info, not stripped


### VM Libraries
Following libraries are symbolic link to libc-2.28.so but are irrelevant

./usr/lib/x86_64-linux-gnu/libc.so.6
./usr/libx32/libc.so.6
./usr/lib32/libc.so.6
./usr/aarch64-linux-gnu/lib/libc.so.6
./var/lib/schroot/chroots/rpizero-bullseye-armhf/usr/lib/arm-linux-gnueabihf/libc.so.6
./var/lib/schroot/chroots/rpi3-bookworm-armhf/usr/lib/arm-linux-gnueabihf/libc.so.6
./var/lib/schroot/chroots/rpizero-buster-armhf/usr/lib/arm-linux-gnueabihf/libc.so.6


other irrelevant libraries
./home/student/opt/x-tools/aarch64-rpi3-linux-gnu/aarch64-rpi3-linux-gnu/sysroot/lib/libc.so.6
./home/student/opt/x-tools/armv6-rpi-linux-gnueabihf/armv6-rpi-linux-gnueabihf/sysroot/lib/libc.so.6
./snap/snapd/20671/lib/x86_64-linux-gnu/libc.so.6
./snap/snapd/20290/lib/x86_64-linux-gnu/libc.so.6
./snap/core20/2105/usr/lib/i386-linux-gnu/libc.so.6
./snap/core20/2105/usr/lib/x86_64-linux-gnu/libc.so.6
./snap/core20/1695/usr/lib/i386-linux-gnu/libc.so.6
./snap/core20/1695/usr/lib/x86_64-linux-gnu/libc.so.6
./snap/core22/1033/usr/lib/i386-linux-gnu/libc.so.6
./snap/core22/1033/usr/lib/x86_64-linux-gnu/libc.so.6

### Used libraries
./home/student/opt/x-tools/armv8-rpi3-linux-gnueabihf/armv8-rpi3-linux-gnueabihf/sysroot/lib/libc.so.6
./var/lib/schroot/chroots/rpi3-bookworm-armhf/lib/ld-linux-armhf.so.3




### Raspberry library 
./usr/lib/arm-linux-gnueabihf/libc.so.6 

version:
GNU C Library (Debian GLIBC 2.36-9+rpt2+deb12u3) stable release version 2.36.

## Note regarding architecture, since our target architecture is ARM based as we can see below, every library used should be ARM based even if our development is done in x86_64 devices.
architecture : 

/usr/lib/arm-linux-gnueabihf/libc.so.6: ELF 32-bit LSB shared object, ARM, EABI5 version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux-armhf.so.3, BuildID[sha1]=42be4e8982da16bbc923ab089ac95f32cbdc5aa9, for GNU/Linux 3.2.0, stripped


### Compiler library
./home/student/opt/x-tools/armv8-rpi3-linux-gnueabihf/armv8-rpi3-linux-gnueabihf/sysroot/lib/libc.so.6

version:
GNU C Library (crosstool-NG UNKNOWN - tttapa/docker-arm-cross-toolchain:armv8-rpi3) stable release version 2.36.




### Runtime libraries


linux-vdso.so.1 (0xf795b000) (Special dynamic library at kernel level)

/usr/lib/arm-linux-gnueabihf/libarmmem-${PLATFORM}.so => /usr/lib/arm-linux-gnueabihf/libarmmem-v8l.so (0xf7930000) (Not a relevant library for lab2)

 

libc.so.6 => /lib/arm-linux-gnueabihf/libc.so.6 (0xf77b7000)
/lib/ld-linux-armhf.so.3 (0xf795c000)

version : GNU C Library (Debian GLIBC 2.36-9+rpt2+deb12u3) stable release version 2.36.
Compiled by GNU CC version 12.2.0.



### Debug library
/var/lib/schroot/chroots/rpi3-bookworm-armhf/lib/ld-linux-armhf.so.3

version:
(Debian GLIBC 2.36-9+rpi1+deb12u3) stable release version 2.36.

### Backwards compatibility
The glibc on raspberry is of version 2.36

The executable should be backwards compatible with Debian Bullseye with some limitations, but not with Debian Buster. It might still work on both, but it isn't guaranteed. If it is imperative to be backwards compatible with both, the glibc version should be 2.31, as that is backwards compatible with 2.28 Buster.

### Benefits of cross-development setup

-Making one codebase for multiple platforms at once, instead of creating a codebase for each platform seperately. 

-Fixes can be applied to all platforms while making changes in the codebase.

-Larger reach of audience since you can target multiple platforms at once.