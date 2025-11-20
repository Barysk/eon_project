#include "./algorithms.cpp"

int main(int argc, char* argv[]) {

	// POL12 FirstFitFit
	Simulator sim_pol_ff = Simulator(
		std::string("./assets/POL12/json_data/pol12net.json"),
		std::string("./assets/POL12/json_data/pol12pat.json")
	);
	USE_ALLOC_FUNCTION(FirstFit, sim_pol_ff);
	sim_pol_ff.setGoalConnections(1e6);
	sim_pol_ff.init();
	sim_pol_ff.run();

	// POL12 ExactFit
	Simulator sim_pol_ef = Simulator(
		std::string("./assets/POL12/json_data/pol12net.json"),
		std::string("./assets/POL12/json_data/pol12pat.json")
	);
	USE_ALLOC_FUNCTION(ExactFit, sim_pol_ef);
	sim_pol_ef.setGoalConnections(1e6);
	sim_pol_ef.init();
	sim_pol_ef.run();

	// // // US26 Zone -- simulate after POL12 works 100% good
	// // US26 FirstFitFit
	// Simulator sim_us_ff = Simulator(
	// 	std::string("./assets/US26/json_data/us26net.json"),
	// 	std::string("./assets/US26/json_data/us26pat.json")
	// );
	// USE_ALLOC_FUNCTION(FirstFit, sim_us_ff);
	// sim_us_ff.setGoalConnections(1e6);
	// sim_us_ff.init();
	// sim_us_ff.run();
	//
	// // US26 ExactFit
	// Simulator sim_us_ef = Simulator(
	// 	std::string("./assets/US26/json_data/us26net.json"),
	// 	std::string("./assets/US26/json_data/us26pat.json")
	// );
	// USE_ALLOC_FUNCTION(ExactFit, sim_us_ef);
	// sim_us_ef.setGoalConnections(1e6);
	// sim_us_ef.init();
	// sim_us_ef.run();

	return 0;
}

