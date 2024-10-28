
# Waffle House Index SRS

## Table of Contents

- [[#Introduction]]
- [[#System Overview]]
- [[#System Architecture & Design]]
- [[#Functional Requirements]]
- [[#Non-Functional Requirements]]
- [[#Data Flow & Modules]]
- [[#Use Case Scenarios]]
- [[#System Constraints]]
- [[#Implementation Plan]]

## Introduction

This project is a **real-time web application** that tracks and displays the **Waffle House Index**, a disaster severity indicator based on the operational status of Waffle House restaurants. The webpage provides an instant view of the index through real-time updates.


## System Overview

A high-level summary of how the system, including how it interacts with external entities such as users, APIs, etc.

## System Architecture & Design

This section will outline the overall architecture and design of the system with diagrams.

## Functional Requirements

This section outlines the core features and functionality of the WHI system.

### Key Features

- Real-time Waffle House Status
- Real-time Waffle House Index
- Geographical visualization
- Real-time data updates
- API Integration
- Disaster alerts

### TO-DO List

#### Simon

**Overall Goal: Implement data collection, URL construction, and API integration.**

1. **Data Gathering**:
	- **Goal**: Gather `{city-state-storeNum}` for each location and storing them in a MongoDB database.
	- **Tasks**:
		- [ ] Automate the extraction of `{city-state-storeNum}` using `Playwright`.
		- [ ] Explore scrolling behavior and identify a strategy to load all requests on the webpage.
			- **Current Roadblock**: Requests for each location only appear once you scroll down.
		- [ ] Confirm that all requests are captured.
		- [ ] Parse the response to retrieve `{city-state-storeNum}`.
2. **Dynamic ID Extraction**:
	- **Goal**: Identify and extract the `dynamic_ID` from network requests.
	- **Tasks**:
		- [ ] Analyze network requests in developer tools to locate the `dynamic_ID`.
		- [ ] Write a `Playwright` script to capture the current request and extract the `dynamic_ID`.
			- **Note**: The `dynamic_ID` will be the same for all store locations per *session*.
		- [ ] Test the script for consistency and handle edge cases when `dyanamic_ID` changes.
		
3. **URL Construction**:
	- **Goal**: Construct request URLs using `{city-state-storeNum}` and `dynamic_ID`.
	- **Tasks**:
		- [ ] Create a script to concatenate `{city-state-storeNum}` and `dynamid_ID` into the *base URL* structure.
			- **Base URL structure**: `https://locations.wafflehouse.com/_next/data/{dynamic_ID}/{city-state-storeNum}.json?slug={city-state-storeNum}`
		- [ ] Validate the constructed URLs for different store locations using sample inputs.

4. **Database Storage**:
	- **Goal**: Store and manage `{city-state-storeNum}` data in MongoDB.
	- **Tasks**:
		- [ ] Set up MongoDB.
		- [ ] Define and create collections and documents for `{city-state-storeNum}` records.'
		- [ ] Implement database insertion logic for new data and update logic for existing records.

##### Notes

The dynamic_ID in the request URL expires after a certain time (to be determined).

**URL Example**:

- `https://locations.wafflehouse.com/_next/data/qvpyngvpagjjpfxlvjfwp/tucson-az-431.json?slug=tucson-az-431`

**Data to Capture**:

- `dyanmic_ID`: `qvpyngvpagjjpfxlvjfwp`
- `city-state-storeNum`: `tucson-az-431`

#### Freddy

- [ ] Parse through HTML and isolate `storeCode`, `city`, and `state`.
- [ ] Start initial front-end

## Non-Functional Requirements

Focuses on how the system performs its functions, addressing these aspects:
- performance
- reliability
- usability
- maintainability
- security

## Data Flow & Modules

This section defines the data flow between different components of the system and describe each modules role.

## Use Case Scenarios

- Real-time referencing for areas severely impacted by weather (hurricanes, tornadoes, etc)
- Monitoring severity of entire regions based off of waffle house operational Status
- Possibly integrate weather map to reference between the two

## System Constraints

Address any technical, hardware, or any other limitations that may affect system's implementation or operation.

## Implementation Plan

# Note: 
The endpoint URL destination is not consistent and changes unpredictlbly. API endpoint used in request_store1718.py no longer returns a valid location and not the approach of using a structured endpoint URL to populate the database no longer is valid

