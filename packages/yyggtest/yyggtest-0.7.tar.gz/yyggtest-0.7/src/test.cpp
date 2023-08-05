#include <pybind11/pybind11.h>
#include <iostream>
#include <armadillo>

namespace py = pybind11;



PYBIND11_MODULE(yyggtest, m) {
    m.doc() = R"pbdoc(
    Pybind11 example plugin
    -----------------------

    .. currentmodule:: python_example

    .. autosummary::
    :toctree: _generate

    add
    subtract
    fourty_two
    )pbdoc";

    
#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
