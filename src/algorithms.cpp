#pragma once
#include "../lib/simulator.hpp"

BEGIN_ALLOC_FUNCTION(FirstFit)
{
	// Define auxiliary variables
	int currentNumberSlots;
	int currentSlotIndex;
	int modulation;
	int requiredSlots;
	std::vector<bool> totalSlots;
	Route currentRoute;
	float routeLength;

	// Iterate through all available routes
	for (int r = 0; r < NUMBER_OF_ROUTES; r++) {
		// Reset slot availability for the current route
		totalSlots = std::vector<bool>(LINK_IN_ROUTE(r, 0)->getSlots(), false);

		// Iterate through each link in the route
		for (int l = 0; l < NUMBER_OF_LINKS(r); l++) {
			// Update totalSlots vector with slot status from each link
			for (int s = 0; s < LINK_IN_ROUTE(r, l)->getSlots(); s++) {
				totalSlots[s] = totalSlots[s] | LINK_IN_ROUTE(r, l)->getSlot(s);
			}
		}

		// Search for a contiguous block of available slots
		currentNumberSlots = 0;
		currentSlotIndex = 0;

		currentRoute = REQ_ROUTE(r);
		modulation = REQ_DISTANCE_ADAPTIVE_MODULATION(currentRoute);
		if (modulation == -1) continue;
		requiredSlots = bitRate.getNumberOfSlots(modulation);
		for (int s = 0; s < totalSlots.size(); s++) {
			if (totalSlots[s] == false) { // Slot is available on all links
				currentNumberSlots++;
			}
			else { // Reset counter if a slot is occupied
				currentNumberSlots = 0;
				currentSlotIndex = s + 1;
			}

			// If a contiguous block of requiredSlots is found, allocate them
			if (currentNumberSlots == requiredSlots) {
				for (int l = 0; l < NUMBER_OF_LINKS(r); l++) {
					ALLOC_SLOTS(LINK_IN_ROUTE_ID(r, l), currentSlotIndex, requiredSlots);
				}
				return ALLOCATED;
			}
		}
	}
	// No suitable slot found in any route
	return NOT_ALLOCATED;
}
END_ALLOC_FUNCTION

BEGIN_ALLOC_FUNCTION(ExactFit) {
	int numberOfSlots;
	int modulation;
	int currentNumberSlots;
	int currentSlotIndex;
	int firstIndex;
	Route currentRoute;
	float routeLength;
	std::vector<bool> totalSlots;
	for (int i = 0; i < NUMBER_OF_ROUTES; i++) {
		totalSlots = std::vector<bool>(LINK_IN_ROUTE(0, 0)->getSlots(), false);
		firstIndex = -1;
		for (int j = 0; j < NUMBER_OF_LINKS(i); j++) {
			for (int k = 0; k < LINK_IN_ROUTE(i, j)->getSlots(); k++) {
				totalSlots[k] = totalSlots[k] | LINK_IN_ROUTE(i, j)->getSlot(k);
			}
		}
		currentNumberSlots = 0;
		currentSlotIndex = 0;
		currentRoute = REQ_ROUTE(i);
		modulation = REQ_DISTANCE_ADAPTIVE_MODULATION(currentRoute);
		if (modulation == -1) continue;
		numberOfSlots = bitRate.getNumberOfSlots(modulation);
		for (int j = 0; j < totalSlots.size(); j++) {
			if (totalSlots[j] == false) {
				currentNumberSlots++;
			} else {
				if (currentNumberSlots == numberOfSlots) {
					for (int j = 0; j < NUMBER_OF_LINKS(i); j++) {
						ALLOC_SLOTS(LINK_IN_ROUTE_ID(i, j), currentSlotIndex, numberOfSlots);
					}
					return ALLOCATED;
				}
				currentNumberSlots = 0;
				currentSlotIndex = j + 1;
			}
			if (firstIndex == -1 && currentNumberSlots > numberOfSlots) {
				firstIndex = currentSlotIndex;
			}
		}
		if (firstIndex != -1) {
			for (int j = 0; j < NUMBER_OF_LINKS(i); j++) {
				ALLOC_SLOTS(LINK_IN_ROUTE_ID(i, j), firstIndex, numberOfSlots);
			}
			return ALLOCATED;
		}
	}
	return NOT_ALLOCATED;
}
END_ALLOC_FUNCTION

