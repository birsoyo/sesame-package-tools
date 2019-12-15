include(default)

[settings]
compiler=apple-clang
compiler.libcxx=libc++
compiler.cppstd=17
os=iOS
os.version=13.0

[build_requires]
ios/0.1.0@sesame/stable
cmake/3.16.1@sesame/stable
ninja/1.9.0@sesame/stable
