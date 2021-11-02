#include <tchem/intcoord.hpp>

int main(size_t argc, const char ** argv) {
    std::cout << "Translate internal coordinate definition in different formats\n\n"
              << "Usage:\n"
              << "    input_format input_IntCoordDef output_format output_IntCoordDef\n";
    tchem::IC::IntCoordSet set(argv[1], argv[2]);
    std::ofstream ofs; ofs.open(argv[4]);
    set.print(ofs, argv[3]);
    ofs.close();
}