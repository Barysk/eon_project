#include "./algorithms.cpp"
#include <cstdio>

// For defining data for tests
struct Scenario{
	double lambda;             // lambda Param type double. It represents the frequency of the arrives.
	double mu;                 // mu Param type doble. It represents the frequency of the departures.
	long long goal_connections; // goal Param type long long. Represents the total number of connections to be simulated.
};

// Just to hold our paths
struct NetworkDataPaths{
	std::string net;
	std::string pat;
};

void print_info() {

}

int main(int argc, char* argv[]) {
	const int NUM_SCENARIOS = 5;
	const std::string BITRATE_PATH = "./assets/bitrate.json";

	const struct Scenario SCENARIOS[NUM_SCENARIOS] = {
		{50.0,   1.0,  500}, // light load
		{75.0,   1.0,  500}, // medium-light load
		{100.0,  1.0,  500}, // medium load
		{125.0,  1.0,  500}, // medium-heavy load
		{150.0,  1.0,  500}  // heavy load
	};

	const struct NetworkDataPaths POL12 = {
		"./assets/POL12/json_data/pol12net.json",
		"./assets/POL12/json_data/pol12pat.json",
	};

	const struct NetworkDataPaths US26 = {
		"./assets/US26/json_data/us26net.json",
		"./assets/US26/json_data/us26pat.json",
	};

	////////////////////
	// POL12 FirstFit //
	////////////////////

	for (size_t i = 0; i < NUM_SCENARIOS; i += 1) {
		double    lambda   = SCENARIOS[i].lambda;
		double    mu       = SCENARIOS[i].mu;
		long long goal_conn = SCENARIOS[i].goal_connections;

		printf("=== Simulation %lu ===\n", i+1);
		printf("Lambda: %.2f, Mu: %.2f, Goal Connections: %.2lli\n", lambda, mu, goal_conn);

		Simulator sim_pol_ff(
			POL12.net,
			POL12.pat,
			BITRATE_PATH,
			EON
		);

		USE_ALLOC_FUNCTION(FirstFit, sim_pol_ff);

		sim_pol_ff.setGoalConnections(goal_conn);
		sim_pol_ff.setLambda(lambda);
		sim_pol_ff.setMu(mu);

		sim_pol_ff.init();
		sim_pol_ff.run();

		printf("Blocking Probability: %f\n\n", sim_pol_ff.getBlockingProbability());
	}

	////////////////////
	// POL12 ExactFit //
	////////////////////

	for (size_t i = 0; i < NUM_SCENARIOS; i += 1) {
		double    lambda   = SCENARIOS[i].lambda;
		double    mu       = SCENARIOS[i].mu;
		long long goal_conn = SCENARIOS[i].goal_connections;

		printf("=== Simulation %lu ===\n", i+1);
		printf("Lambda: %.2f, Mu: %.2f, Goal Connections: %.2lli\n", lambda, mu, goal_conn);

		Simulator sim_pol_ff(
			POL12.net,
			POL12.pat,
			BITRATE_PATH,
			EON
		);

		USE_ALLOC_FUNCTION(ExactFit, sim_pol_ff);

		sim_pol_ff.setGoalConnections(goal_conn);
		sim_pol_ff.setLambda(lambda);
		sim_pol_ff.setMu(mu);

		sim_pol_ff.init();
		sim_pol_ff.run();

		printf("Blocking Probability: %f\n\n", sim_pol_ff.getBlockingProbability());
	}

	///////////////////
	// US26 FirstFit //
	///////////////////

	for (size_t i = 0; i < NUM_SCENARIOS; i += 1) {
		double    lambda   = SCENARIOS[i].lambda;
		double    mu       = SCENARIOS[i].mu;
		long long goal_conn = SCENARIOS[i].goal_connections;

		printf("=== Simulation %lu ===\n", i+1);
		printf("Lambda: %.2f, Mu: %.2f, Goal Connections: %.2lli\n", lambda, mu, goal_conn);

		Simulator sim_pol_ff(
			US26.net,
			US26.pat,
			BITRATE_PATH,
			EON
		);

		USE_ALLOC_FUNCTION(FirstFit, sim_pol_ff);

		sim_pol_ff.setGoalConnections(goal_conn);
		sim_pol_ff.setLambda(lambda);
		sim_pol_ff.setMu(mu);

		sim_pol_ff.init();
		sim_pol_ff.run();

		printf("Blocking Probability: %f\n\n", sim_pol_ff.getBlockingProbability());
	}

	///////////////////
	// US26 ExactFit //
	///////////////////

	for (size_t i = 0; i < NUM_SCENARIOS; i += 1) {
		double    lambda   = SCENARIOS[i].lambda;
		double    mu       = SCENARIOS[i].mu;
		long long goal_conn = SCENARIOS[i].goal_connections;

		printf("=== Simulation %lu ===\n", i+1);
		printf("Lambda: %.2f, Mu: %.2f, Goal Connections: %.2lli\n", lambda, mu, goal_conn);

		Simulator sim_pol_ff(
			US26.net,
			US26.pat,
			BITRATE_PATH,
			EON
		);

		USE_ALLOC_FUNCTION(ExactFit, sim_pol_ff);

		sim_pol_ff.setGoalConnections(goal_conn);
		sim_pol_ff.setLambda(lambda);
		sim_pol_ff.setMu(mu);

		sim_pol_ff.init();
		sim_pol_ff.run();

		printf("Blocking Probability: %f\n\n", sim_pol_ff.getBlockingProbability());
	}

	return 0;
}

