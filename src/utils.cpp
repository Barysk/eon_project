#include <string>

// For defining data for tests
struct Scenario {
	double lambda;              // lambda Param type double. It represents the frequency of the arrives.
	double mu;                  // mu Param type doble. It represents the frequency of the departures.
	long long goal_connections; // goal Param type long long. Represents the total number of connections to be simulated.
};

// Just to hold our paths
struct NetworkDataPaths {
	std::string net;
	std::string pat;
};

// helper func for finding a size of an array
template <typename T, std::size_t N>
constexpr std::size_t len(const T (&)[N]) {
	return N;
}

