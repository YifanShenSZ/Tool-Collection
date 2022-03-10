# rebuild c++ tools
cd cpp
for cpp_tool in translate_IntCoordDef cart2int int2cart vibration; do
    echo
    echo "Entre "$cpp_tool
    cd $cpp_tool/build
    cmake --build .
    cd ../..
done
cd ..
