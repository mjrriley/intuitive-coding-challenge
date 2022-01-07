#include <pybind11/pybind11.h>
#include "embedded.h"

namespace py = pybind11;

PYBIND11_MODULE(embeddedPy, m) {
    py::class_<SystemParameters>(m, "SystemParameters")
        .def(py::init<>())
        .def_readwrite("node_id", &SystemParameters::node_id)
        .def_readwrite("system_name", &SystemParameters::system_name)
        .def_readwrite("system_time", &SystemParameters::system_time)
        .def_readwrite("active", &SystemParameters::active);

    py::enum_<UpdateStatus>(m, "UpdateStatus")
        .value("DONE", UpdateStatus::DONE)
        .value("FAILED", UpdateStatus::FAILED)
        .export_values();

    m.def("getSystemInstance", &System::getInstance, py::return_value_policy::reference);

    py::class_<System>(m, "System")
        .def("write", &System::write)
        .def("read", &System::read);
}
