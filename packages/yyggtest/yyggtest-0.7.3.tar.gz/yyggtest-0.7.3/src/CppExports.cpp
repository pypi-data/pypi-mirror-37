#include <pybind11/pybind11.h>
#include <iostream>
#include <armadillo>

namespace py = pybind11;

int add(int i, int j){
    return i + j;
}



PYBIND11_MODULE(cpp_exports, m) {
    m.doc() = R"pbdoc(
    Pybind11 example plugin
    -----------------------

    .. currentmodule:: python_example

    .. autosummary::
    :toctree: _generate

    add
    asdqweasd
    )pbdoc";

    m.def("thing", [](int i){ return i; }, "a description");

    m.def("add", &add, "A function to add two numbers");

    
#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
