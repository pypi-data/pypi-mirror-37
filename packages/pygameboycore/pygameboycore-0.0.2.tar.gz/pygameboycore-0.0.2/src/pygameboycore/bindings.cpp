#include <bindings.hpp>
#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MODULE(pygameboycore, m)
{
  py::class_<gb::Pixel>(m, "Pixel")
    .def(py::init<>())
    .def_readwrite("r", &gb::Pixel::r)
    .def_readwrite("g", &gb::Pixel::g)
    .def_readwrite("b", &gb::Pixel::b);

  py::enum_<gb::Joy::Key>(m, "JoypadKey")
    .value("KEY_RIGHT",  gb::Joy::Key::RIGHT)
    .value("KEY_LEFT",   gb::Joy::Key::LEFT)
    .value("KEY_UP",     gb::Joy::Key::UP)
    .value("KEY_DOWN",   gb::Joy::Key::DOWN)
    .value("KEY_A",      gb::Joy::Key::A)
    .value("KEY_B",      gb::Joy::Key::B)
    .value("KEY_SELECT", gb::Joy::Key::SELECT)
    .value("KEY_START",  gb::Joy::Key::START)
    .export_values();

  py::enum_<PyGameboyCore::KeyAction>(m, "KeyAction")
    .value("ACTION_PRESS", PyGameboyCore::KeyAction::PRESS)
    .value("ACTION_RELEASE", PyGameboyCore::KeyAction::RELEASE)
    .export_values();

  py::class_<PyGameboyCore>(m, "GameboyCore")
    .def(py::init<>())
    .def("update", &PyGameboyCore::update)
    .def("open", &PyGameboyCore::open)
    .def("input", &PyGameboyCore::input)
    .def(
      "register_scanline_callback",
      &PyGameboyCore::register_scanline_callback
    )
    .def(
      "register_vblank_callback",
      &PyGameboyCore::register_vblank_callback
    );
}
