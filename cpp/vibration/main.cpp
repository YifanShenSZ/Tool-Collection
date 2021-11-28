#include <CppLibrary/argparse.hpp>
#include <CppLibrary/utility.hpp>
#include <CppLibrary/chemistry.hpp>

#include <tchem/utility.hpp>
#include <tchem/intcoord.hpp>
#include <tchem/chemistry.hpp>

argparse::ArgumentParser parse_args(const size_t & argc, const char ** & argv) {
    CL::utility::echo_command(argc, argv, std::cout);
    std::cout << '\n';
    argparse::ArgumentParser parser("vibration: Compute normal mode from internal coordinate Hessian");

    // required arguments
    parser.add_argument("-f","--format",  1, false, "internal coordinate definition format (Columbus7, default)");
    parser.add_argument("-i","--IC"    ,  1, false, "internal coordinate definition file");
    parser.add_argument("-x","--xyz"   ,  1, false, "input xyz geometry");
    parser.add_argument("-m","--mass",    1, false, "the masses of atoms");
    parser.add_argument("-H","--Hessian", 1, false, "internal coordinate Hessian");

    // optional argument
    parser.add_argument("-o","--output", 1, true, "output file name (default = avogadro.log)");

    parser.parse_args(argc, argv);
    return parser;
}

int main(size_t argc, const char ** argv) {
    std::cout << "Compute normal mode from internal coordinate Hessian\n";
    argparse::ArgumentParser args = parse_args(argc, argv);
    CL::utility::show_time(std::cout);
    std::cout << '\n';

    std::string format = args.retrieve<std::string>("format");
    std::string IC     = args.retrieve<std::string>("IC");
    tchem::IC::IntCoordSet icset(format, IC);

    std::string geom_file = args.retrieve<std::string>("xyz"),
                mass_file = args.retrieve<std::string>("mass");
    CL::chem::xyz_mass<double> geom(geom_file, mass_file, true);

    at::Tensor Hessian = tchem::utility::read_vector(args.retrieve<std::string>("Hessian"));
    int64_t intdim = sqrt(Hessian.numel());
    Hessian.resize_({intdim, intdim});

    std::vector<double> coords = geom.coords();
    at::Tensor r = at::from_blob(coords.data(), coords.size(), at::TensorOptions().dtype(torch::kFloat64));
    at::Tensor q, J;
    std::tie(q, J) = icset.compute_IC_J(r);
    tchem::chem::IntNormalMode intvib(geom.masses(), J, Hessian);
    intvib.kernel();

    std::string output = "avogadro.log";
    if (args.gotArgument("output")) output = args.retrieve<std::string>("output");
    auto freqs = tchem::utility::tensor2vector(intvib.frequency());
    auto modes = tchem::utility::tensor2matrix(intvib.cartmode());
    CL::chem::xyz_vib<double> avogadro(geom.symbols(), geom.coords(), freqs, modes, true);
    avogadro.print(output);

    CL::utility::show_time(std::cout);
    std::cout << "Mission success\n";
}