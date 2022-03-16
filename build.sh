cpp_tools=(translate_IntCoordDef cart2int int2cart vibration)

# build c++ tools
cd cpp
for cpp_tool in "${cpp_tools[@]}"; do
    echo
    echo "Entre "$cpp_tool
    cd $cpp_tool
    # build
    if [ -d build ]; then rm -r build; fi
    mkdir build
    cd build
    cmake -DCMAKE_C_COMPILER=icc -DCMAKE_CXX_COMPILER=icpc -DCMAKE_Fortran_COMPILER=ifort ..
    cmake --build .
    cd ..
    # finish
    cd ..
done
cd ..

# link every executable to bin/
if [ -d bin ]; then rm -r bin; fi
mkdir bin
cd bin
# link c++ tools
for cpp_tool in "${cpp_tools[@]}"; do
    ln -s ../cpp/$cpp_tool/build/$cpp_tool.exe
done
# finish
cd ..
