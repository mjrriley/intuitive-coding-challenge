#include <pybind11/pybind11.h>
#include "embedded.h"

namespace py = pybind11;

enum class EWriteStatus
{
    NONE = 0,
    REQUESTED = 1,
    UPDATING = 2,
    DONE = 3,
    FAILED = 4
};

class WriteStatus
{
public:

    static WriteStatus& getInstance()
    {
        static WriteStatus instance;
        return instance;
    }

    EWriteStatus & get()
    {
        return status_;
    }

    void set(EWriteStatus const & status)
    {
        status_ = status;
    }

    ~WriteStatus() = default;

private:
    WriteStatus():
        status_(EWriteStatus::NONE)
    {
    }

    EWriteStatus status_;
};

PYBIND11_MODULE(embeddedPy, m) {
    // From embedded.h
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

    m.def("getSystemStatus", []() -> SystemParameters const & {
        return System::getInstance().read();
    });

    m.def("writeSystemParameters", [](SystemParameters const & params) -> UpdateStatus {
        py::gil_scoped_release release;
        auto i = System::getInstance().write(params);
        py::gil_scoped_acquire acquire;
        return i;
    });

    // EWriteStatus && WriteStatus
    py::enum_<EWriteStatus>(m, "EWriteStatus")
        .value("NONE", EWriteStatus::NONE)
        .value("REQUESTED", EWriteStatus::REQUESTED)
        .value("UPDATING", EWriteStatus::UPDATING)
        .value("DONE", EWriteStatus::DONE)
        .value("FAILED", EWriteStatus::FAILED);

    m.def("getWriteStatus", []() -> EWriteStatus const & {
        return WriteStatus::getInstance().get();
    });

    m.def("setWriteStatus", [](EWriteStatus const & status) {
        WriteStatus::getInstance().set(status);
    });
}
