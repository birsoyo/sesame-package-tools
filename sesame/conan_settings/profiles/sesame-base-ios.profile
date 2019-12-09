include(default)

[settings]
compiler=apple-clang
compiler.version=11.0
compiler.libcxx=libc++
compiler.cppstd=17
os=iOS
os.version=13.0

[build_requires]
cmake/3.16.0@sesame/testing
ninja/1.9.0@sesame/testing
