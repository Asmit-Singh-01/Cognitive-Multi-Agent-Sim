#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <cstdlib>
#include <ctime>

namespace py = pybind11;

class FastEnvEngine {
private:
    int grid_size;
    int num_agents;
    int num_resources;
    std::vector<int> agent_positions;    // Flattened 1D array: [x0, y0, x1, y1, ...]
    std::vector<int> resource_positions; // Flattened 1D array: [rx0, ry0, rx1, ry1, ...]

public:
    FastEnvEngine(int size, int agents, int resources) {
        grid_size = size;
        num_agents = agents;
        num_resources = resources;
        
        agent_positions.resize(num_agents * 2, 0);
        resource_positions.resize(num_resources * 2, 0);
        
        std::srand(std::time(nullptr)); // Seed for random placement
        reset();
    }

    void reset() {
        // Randomly scatter agents on the grid
        for (int i = 0; i < num_agents * 2; ++i) {
            agent_positions[i] = std::rand() % grid_size;
        }
        // Randomly scatter resources
        for (int i = 0; i < num_resources * 2; ++i) {
            resource_positions[i] = std::rand() % grid_size;
        }
    }

    std::vector<int> get_agent_positions() { return agent_positions; }
    std::vector<int> get_resource_positions() { return resource_positions; }

    // Blazing fast C++ logic for processing steps, collisions, and rewards
    std::vector<double> step(const std::vector<int>& actions) {
        std::vector<double> rewards(num_agents, 0.0);

        // 1. Process Actions and Update Positions
        for (int i = 0; i < num_agents; ++i) {
            int act = actions[i];
            int ax = agent_positions[i * 2];
            int ay = agent_positions[i * 2 + 1];

            if (act == 0 && ax > 0) ax--;                  // Move Up
            else if (act == 1 && ax < grid_size - 1) ax++; // Move Down
            else if (act == 2 && ay > 0) ay--;              // Move Left
            else if (act == 3 && ay < grid_size - 1) ay++;  // Move Right
            // Action 4 is 'Stay' (no position change)

            agent_positions[i * 2] = ax;
            agent_positions[i * 2 + 1] = ay;
        }

        // 2. Resource Gathering Logic
        for (int i = 0; i < num_agents; ++i) {
            int ax = agent_positions[i * 2];
            int ay = agent_positions[i * 2 + 1];

            for (int j = 0; j < num_resources; ++j) {
                int rx = resource_positions[j * 2];
                int ry = resource_positions[j * 2 + 1];

                // If agent steps on resource
                if (ax == rx && ay == ry) {
                    rewards[i] += 10.0; // High reward for collection
                    
                    // Respawn resource at a new random location
                    resource_positions[j * 2] = std::rand() % grid_size;
                    resource_positions[j * 2 + 1] = std::rand() % grid_size;
                }
            }
            
            // Standard time step penalty to force efficiency
            rewards[i] -= 0.1;
        }

        // 3. High-Speed Collision Matrix Check (Agent vs Agent)
        for (int i = 0; i < num_agents; ++i) {
            for (int j = i + 1; j < num_agents; ++j) {
                if (agent_positions[i * 2] == agent_positions[j * 2] &&
                    agent_positions[i * 2 + 1] == agent_positions[j * 2 + 1]) {
                    rewards[i] -= 5.0; // Collision penalty
                    rewards[j] -= 5.0;
                }
            }
        }

        return rewards;
    }
};

// Expose the module to Python via pybind11
PYBIND11_MODULE(fast_env, m) {
    py::class_<FastEnvEngine>(m, "FastEnvEngine")
        .def(py::init<int, int, int>())
        .def("reset", &FastEnvEngine::reset)
        .def("step", &FastEnvEngine::step)
        .def("get_agent_positions", &FastEnvEngine::get_agent_positions)
        .def("get_resource_positions", &FastEnvEngine::get_resource_positions);
}
