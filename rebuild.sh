cpp_tools=(translate_IntCoordDef cart2int int2cart cart2SASIC)

# rebuild c++ tools
cd cpp
for cpp_tool in "${cpp_tools[@]}"; do
    echo
    echo "Entre "$cpp_tool
    cd $cpp_tool/build
    cmake --build .
    cd ../..
done
cd ..
