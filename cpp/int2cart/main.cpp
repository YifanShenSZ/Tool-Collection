#include <CppLibrary/argparse.hpp>
#include <CppLibrary/utility.hpp>
#include <CppLibrary/chemistry.hpp>

#include <Foptim/trust_region.hpp>

#include <tchem/utility.hpp>
#include <tchem/intcoord.hpp>

argparse::ArgumentParser parse_args(const size_t & argc, const char ** & argv) {
    CL::utility::echo_command(argc, argv, std::cout);
    std::cout << '\n';
    argparse::ArgumentParser parser("cart2int: Convert geometry from Cartesian coordinate to internal coordinate");

    // required arguments
    parser.add_argument("-f","--format"  , 1, false, "internal coordinate definition format (Columbus7, default)");
    parser.add_argument("-i","--IC"      , 1, false, "internal coordinate definition file");
    parser.add_argument("-g","--geometry", 1, false, "input internal coordinate geometry");
    parser.add_argument("-x","--xyz"     , 1, false, "initial guess xyz geometry");

    // optional argument
    parser.add_argument("-o","--output"  , 1, true, "output xyz geometry (default = `input`.xyz)");

    parser.parse_args(argc, argv);
    return parser;
}

at::Tensor int2cart(const at::Tensor & q, const at::Tensor & init_guess,
const std::shared_ptr<tchem::IC::IntCoordSet> & _intcoordset);

int main(size_t argc, const char ** argv) {
    std::cout << "Convert geometry from Cartesian coordinate to symmetry adapted and scaled internal coordinate\n";
    argparse::ArgumentParser args = parse_args(argc, argv);
    CL::utility::show_time(std::cout);
    std::cout << '\n';

    std::string format = args.retrieve<std::string>("format");
    std::string IC     = args.retrieve<std::string>("IC");
    auto icset = std::make_shared<tchem::IC::IntCoordSet>(format, IC);

    std::string q_file = args.retrieve<std::string>("geometry");
    at::Tensor q = tchem::utility::read_vector(q_file);

    CL::chem::xyz<double> init_geom(args.retrieve<std::string>("xyz"), true);
    std::vector<double> init_coords = init_geom.coords();
    at::Tensor init_r = at::from_blob(init_coords.data(), init_coords.size(), at::TensorOptions().dtype(torch::kFloat64));

    at::Tensor r = int2cart(q, init_r, icset);

    std::vector<double> final_coords = init_coords;
    std::memcpy(final_coords.data(), r.data_ptr<double>(), r.numel() * sizeof(double));
    CL::chem::xyz<double> output_geom(init_geom.symbols(), final_coords, true);
    std::ofstream ofs;
    if (args.gotArgument("output")) ofs.open(args.retrieve<std::string>("output"));
    else ofs.open(CL::utility::split(q_file, '.')[0] + ".xyz");
    output_geom.print(ofs);
    ofs.close();

    CL::utility::show_time(std::cout);
    std::cout << "Mission success\n";
}