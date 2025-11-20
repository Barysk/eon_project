#include "./algorithms.cpp"
#include "./utils.cpp"

int main(int argc, char* argv[]) {

	const struct Scenario SCENARIOS[5] = {
		// Lambda   Mu    Goal Connections
		{   50.0,   1.0,  500 }, // light load
		{   75.0,   1.0,  500 }, // medium-light load
		{  100.0,   1.0,  500 }, // medium load
		{  125.0,   1.0,  500 }, // medium-heavy load
		{  150.0,   1.0,  500 }  // heavy load
	};

	const std::string BITRATE_PATH = "./assets/bitrate.json";

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

	for (size_t i = 0; i < len(SCENARIOS); i += 1) {
		double    lambda    = SCENARIOS[i].lambda;
		double    mu        = SCENARIOS[i].mu;
		long long goal_conn = SCENARIOS[i].goal_connections;

		printf("=== Simulation %lu ===\n", i+1);
		printf("Lambda: %.2f, Mu: %.2f, Goal Connections: %.2lli\n", lambda, mu, goal_conn);

		Simulator sim(
			POL12.net,
			POL12.pat,
			BITRATE_PATH,
			EON
		);

		USE_ALLOC_FUNCTION(FirstFit, sim);

		sim.setGoalConnections(goal_conn);
		sim.setLambda(lambda);
		sim.setMu(mu);

		sim.init();
		sim.run();

		printf("Blocking Probability: %f\n\n", sim.getBlockingProbability());
	}

	////////////////////
	// POL12 ExactFit //
	////////////////////

	for (size_t i = 0; i < len(SCENARIOS); i += 1) {
		double    lambda    = SCENARIOS[i].lambda;
		double    mu        = SCENARIOS[i].mu;
		long long goal_conn = SCENARIOS[i].goal_connections;

		printf("=== Simulation %lu ===\n", i+1);
		printf("Lambda: %.2f, Mu: %.2f, Goal Connections: %.2lli\n", lambda, mu, goal_conn);

		Simulator sim(
			POL12.net,
			POL12.pat,
			BITRATE_PATH,
			EON
		);

		USE_ALLOC_FUNCTION(ExactFit, sim);

		sim.setGoalConnections(goal_conn);
		sim.setLambda(lambda);
		sim.setMu(mu);

		sim.init();
		sim.run();

		printf("Blocking Probability: %f\n\n", sim.getBlockingProbability());
	}

	///////////////////
	// US26 FirstFit //
	///////////////////

	for (size_t i = 0; i < len(SCENARIOS); i += 1) {
		double    lambda    = SCENARIOS[i].lambda;
		double    mu        = SCENARIOS[i].mu;
		long long goal_conn = SCENARIOS[i].goal_connections;

		printf("=== Simulation %lu ===\n", i+1);
		printf("Lambda: %.2f, Mu: %.2f, Goal Connections: %.2lli\n", lambda, mu, goal_conn);

		Simulator sim(
			US26.net,
			US26.pat,
			BITRATE_PATH,
			EON
		);

		USE_ALLOC_FUNCTION(FirstFit, sim);

		sim.setGoalConnections(goal_conn);
		sim.setLambda(lambda);
		sim.setMu(mu);

		sim.init();
		sim.run();

		printf("Blocking Probability: %f\n\n", sim.getBlockingProbability());
	}

	///////////////////
	// US26 ExactFit //
	///////////////////

	for (size_t i = 0; i < len(SCENARIOS); i += 1) {
		double    lambda    = SCENARIOS[i].lambda;
		double    mu        = SCENARIOS[i].mu;
		long long goal_conn = SCENARIOS[i].goal_connections;

		printf("=== Simulation %lu ===\n", i+1);
		printf("Lambda: %.2f, Mu: %.2f, Goal Connections: %.2lli\n", lambda, mu, goal_conn);

		Simulator sim(
			US26.net,
			US26.pat,
			BITRATE_PATH,
			EON
		);

		USE_ALLOC_FUNCTION(ExactFit, sim);

		sim.setGoalConnections(goal_conn);
		sim.setLambda(lambda);
		sim.setMu(mu);

		sim.init();
		sim.run();

		printf("Blocking Probability: %f\n\n", sim.getBlockingProbability());
	}

	return 0;
}
