include(default)

[settings]
compiler=apple-clang
compiler.libcxx=libc++
compiler.cppstd=17
os=Macos
os.version=10.14

[build_requires]
cmake/3.16.1@sesame/testing
ninja/1.9.0@sesame/testing
