#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <random>
#include <vector>
#include <string>

namespace py = pybind11;

class PhysicsEngine {
private:
    std::mt19937 gen;
    std::normal_distribution<double> dist;

public:
    PhysicsEngine() : gen(std::random_device{}()), dist(0.0, 1.0) {}

    // Yeh function Python se agents ke coordinates aur unki strategy lega,
    // aur C++ ke andar high-speed random movement calculate karke return karega.
    py::array_t<double> update_positions(py::array_t<double> current_positions, py::list strategies) {
        py::buffer_info buf = current_positions.request();
        if (buf.ndim != 2 || buf.shape[1] != 2) {
            throw std::runtime_error("Input shapes must be (N, 2) dimensions.");
        }

        double* ptr = static_cast<double*>(buf.ptr);
        size_t num_agents = buf.shape[0];

        // Output dynamic array taiyar karo
        auto result = py::array_t<double>({num_agents, (size_t)2});
        double* res_ptr = static_cast<double*>(result.request().ptr);

        for (size_t i = 0; i < num_agents; ++i) {
            std::string strategy = py::cast<std::string>(strategies[i]);
            double dx = dist(gen);
            double dy = dist(gen);

            double x = ptr[i * 2];
            double y = ptr[i * 2 + 1];

            // C++ High Speed Physics Movement
            if (strategy == "greedy") {
                x += dx * 2.5;
                y += dy * 2.5;
            } else {
                x += dx * 0.8;
                y += dy * 0.8;
            }

            // Boundary Condition (0 se 100 ki boundary me agents ko band rakhna)
            if (x < 0) x = 0; if (x > 100) x = 100;
            if (y < 0) y = 0; if (y > 100) y = 100;

            res_ptr[i * 2] = x;
            res_ptr[i * 2 + 1] = y;
        }

        return result;
    }
};

// pybind11 ke zariye C++ class ko python module "physics_core" me export karna
PYBIND11_MODULE(physics_core, m) {
    py::class_<PhysicsEngine>(m, "PhysicsEngine")
        .def(py::init<>())
        .def("update_positions", &PhysicsEngine::update_positions);
}
